import os
import time
from abc import ABC, abstractmethod
from datetime import datetime

import yaml
from thales_remote.script_wrapper import PotentiostatMode
from thales_remote.script_wrapper import ThalesRemoteScriptWrapper

from autothalix.logging import logger
from autothalix.utils import write_dict_to_csv, safe_pot


class BaseMeasurement(ABC):
    def __init__(self, wr_connection: ThalesRemoteScriptWrapper, measurement_id: str, **kwargs):
        """
        :param wr_connection: ThalesRemoteScriptWrapper object to communicate with Thales. You can create it with
            initialize_experiment() function. See autothalix.utils
        :param kwargs: For required parameters look into attribute "parameters" or into baseline file
        :param measurement_id: Unique identifier of the measurement. It will be used in filename with results
        """
        self.load_baseline()  # sets default parameters for a measurement
        self.current_datetime = datetime.today().strftime('%d_%m_%Y_%H_%M_%S')
        self.measurement_id = measurement_id
        for key, value in kwargs.items():
            setattr(self, key, value)
        self._check_parameters()
        self.wr_connection = wr_connection

    def _check_connection(self):
        return self.wr_connection._remote_connection.isConnectedToTerm()

    def _check_parameters(self):
        """Checks if all mandatory parameters are set"""
        for parameter in self.parameters:
            if not hasattr(self, parameter):
                raise ValueError(f'Parameter {parameter} is not set. Check if this parameters in '
                                 f'baseline file {self._baseline_path} and if it is set in the script.')

    @property
    def _baseline_path(self):
        return 'baseline.yaml'

    def load_baseline(self):
        """ Loads baseline parameters from baseline.yaml file """
        with open('baseline.yaml', 'r') as file:
            data = yaml.safe_load(file)[self.measurement_name]
        for parameter_dict in data:
            parameter_value = list(parameter_dict.values())[0]
            parameter_name = list(parameter_dict.keys())[0]
            setattr(self, parameter_name, parameter_value)

    @property
    def _output_filename(self):
        return f"{self.measurement_name}_{self.measurement_id}_{self.current_datetime}"

    @property
    def _run_message(self):
        message = f"Running {self.__str__()} with following parameters:\n"
        for parameter in self.parameters:
            message += f"\t{parameter}: {getattr(self, parameter)}\n"
        return message

    def __str__(self):
        return self._measurement_name

    @property
    def measurement_name(self):
        """
        Name of the experiment
        """
        return self._measurement_name

    def run(self):
        """
        Runs the measurement.

        First checks if connection is established, then sends parameters to the potentiostat and
        starts the measurement.

        :return: bool
            Returns True if measurement was successful.

        :raises ConnectionError:
            If connection is not established, raises ConnectionError with message
            'Connection is not established. Check that connection is established and try again.'
        """
        if self._check_connection():
            logger.info(self._run_message)
            self._send_parameters()
            self._start_measurements()
        else:
            raise ConnectionError('Connection is not established. Check that connection is established and try again.')
        return True

    @property
    @abstractmethod
    def parameters(self):
        pass

    @abstractmethod
    def _start_measurements(self):
        pass

    @abstractmethod
    def _send_parameters(self):
        pass

    @property
    def potentiostat_mode(self):
        return self._PotentiostatMode

    @potentiostat_mode.setter
    def potentiostat_mode(self, value: str):
        mapping = {
            'pseudogalvanostatic': PotentiostatMode.POTMODE_PSEUDOGALVANOSTATIC,
            'galvanostatic': PotentiostatMode.POTMODE_GALVANOSTATIC,
            'potentiostatic': PotentiostatMode.POTMODE_POTENTIOSTATIC,
        }

        self._PotentiostatMode = mapping[str.lower(value)]


class CyclicVoltammetry(BaseMeasurement):
    """
    Cyclic Voltammetry measurement class. Inherits from BaseMeasurement class."""
    _measurement_name = 'cv'
    _measurement_full_name = 'Cyclic Voltammetry'

    @property
    def parameters(self):
        """Returns a list of mandatory parameters for CV measurement"""
        return [
            'counter',
            'cycles',
            'end_hold_time',
            'end_potential',
            'lower_reversing_potential',
            'naming',
            'maximum_current',
            'minimum_current',
            'output_path',
            'ohmic_drop',
            'samples_per_cycle',
            'scan_rate',
            'start_hold_time',
            'start_potential',
            'upper_reversing_potential',
            'analog_function_generator',
            'auto_restart_at_current_overflow',
            'auto_restart_at_current_underflow'
        ]

    def _send_parameters(self):
        self.wr_connection.setCVCounter(self.counter)
        self.wr_connection.setCVOutputPath(self.output_path)
        self.wr_connection.setCVOutputFileName(self._output_filename)
        self.wr_connection.setCVNaming(self.naming)
        self.wr_connection.setCVStartPotential(self.start_potential)
        self.wr_connection.setCVUpperReversingPotential(self.upper_reversing_potential)
        self.wr_connection.setCVLowerReversingPotential(self.lower_reversing_potential)
        self.wr_connection.setCVEndPotential(self.end_potential)
        self.wr_connection.setCVStartHoldTime(self.start_hold_time)
        self.wr_connection.setCVEndHoldTime(self.end_hold_time)
        self.wr_connection.setCVCycles(self.cycles)
        self.wr_connection.setCVSamplesPerCycle(self.samples_per_cycle)
        self.wr_connection.setCVScanRate(self.scan_rate)
        self.wr_connection.setCVMaximumCurrent(self.maximum_current)
        self.wr_connection.setCVMinimumCurrent(self.minimum_current)
        self.wr_connection.setCVOhmicDrop(self.ohmic_drop)
        self.wr_connection.enableCVAnalogFunctionGenerator(self.analog_function_generator)
        self.wr_connection.enableCVAutoRestartAtCurrentOverflow(self.auto_restart_at_current_overflow)
        self.wr_connection.enableCVAutoRestartAtCurrentUnderflow(self.auto_restart_at_current_underflow)

    def _start_measurements(self):
        self.wr_connection.disableCVAutoRestartAtCurrentOverflow()
        self.wr_connection.disableCVAutoRestartAtCurrentUnderflow()
        self.wr_connection.disableCVAnalogFunctionGenerator()
        self.wr_connection.checkCVSetup()
        self.wr_connection.measureCV()


class LinearSweepVoltammetry(BaseMeasurement):
    _measurement_name = 'lsv'
    _measurement_full_name = 'Linear Sweep Voltammetry'

    @property
    def parameters(self):
        """Returns a list of mandatory parameters for LSV measurement"""
        return [
            'absolute_tolerance',
            'counter',
            'first_edge_potential',
            'first_edge_potential_relation',
            'fourth_edge_potential',
            'fourth_edge_potential_relation',
            'maximum_current',
            'maximum_waiting_time',
            'minimum_current',
            'minimum_waiting_time',
            'naming',
            'ohmic_drop',
            'output_path',
            'potential_resolution',
            'relative_tolerance',
            'scan_rate',
            'second_edge_potential',
            'second_edge_potential_relation',
            'sweep_mode',
            'third_edge_potential',
            'third_edge_potential_relation',
        ]

    def _send_parameters(self):
        self.wr_connection.setIEAbsoluteTolerance(self.absolute_tolerance)
        self.wr_connection.setIECounter(self.counter)
        self.wr_connection.setIEFirstEdgePotential(self.first_edge_potential)
        self.wr_connection.setIEFirstEdgePotentialRelation(self.first_edge_potential_relation)
        self.wr_connection.setIEFourthEdgePotential(self.fourth_edge_potential)
        self.wr_connection.setIEFourthEdgePotentialRelation(self.fourth_edge_potential_relation)
        self.wr_connection.setIEMaximumCurrent(self.maximum_current)
        self.wr_connection.setIEMaximumWaitingTime(self.maximum_waiting_time)
        self.wr_connection.setIEMinimumCurrent(self.minimum_current)
        self.wr_connection.setIEMinimumWaitingTime(self.minimum_waiting_time)
        self.wr_connection.setIENaming(self.naming)
        self.wr_connection.setIEOhmicDrop(self.ohmic_drop)
        self.wr_connection.setIEOutputFileName(self._output_filename)
        self.wr_connection.setIEOutputPath(self.output_path)
        self.wr_connection.setIEPotentialResolution(self.potential_resolution)
        self.wr_connection.setIERelativeTolerance(self.relative_tolerance)
        self.wr_connection.setIEScanRate(self.scan_rate)
        self.wr_connection.setIESecondEdgePotential(self.second_edge_potential)
        self.wr_connection.setIESecondEdgePotentialRelation(self.second_edge_potential_relation)
        self.wr_connection.setIESweepMode(self.sweep_mode)
        self.wr_connection.setIEThirdEdgePotential(self.third_edge_potential)
        self.wr_connection.setIEThirdEdgePotentialRelation(self.third_edge_potential_relation)

    def _start_measurements(self):
        self.wr_connection.checkIESetup()
        self.wr_connection.measureIE()


class ElectrochemicalImpedanceSpectroscopy(BaseMeasurement):
    """ Electrochemical Impedance Spectroscopy measurement class"""

    _measurement_name = 'eis'
    _measurement_full_name = 'Electrochemical Impedance Spectroscopy'

    def __str__(self):
        return self._measurement_name

    def _send_parameters(self):
        self.wr_connection.setPotentiostatMode(self.potentiostat_mode)
        self.wr_connection.setAmplitude(self.amplitude)
        self.wr_connection.setPotential(self.potential)
        self.wr_connection.setLowerFrequencyLimit(self.lower_frequency_limit)
        self.wr_connection.setStartFrequency(self.start_frequency)
        self.wr_connection.setUpperFrequencyLimit(self.upper_frequency_limit)
        self.wr_connection.setLowerNumberOfPeriods(self.lower_number_of_periods)
        self.wr_connection.setLowerStepsPerDecade(self.lower_steps_per_decade)
        self.wr_connection.setUpperNumberOfPeriods(self.upper_number_of_periods)
        self.wr_connection.setUpperStepsPerDecade(self.upper_steps_per_decade)
        self.wr_connection.setScanDirection(self.scan_direction)
        self.wr_connection.setScanStrategy(self.scan_strategy)
        self.wr_connection.setEISOutputPath(self.output_path)
        self.wr_connection.setEISOutputFileName(self._output_filename)
        self.wr_connection.setEISNaming(self.naming)

    @property
    def parameters(self):
        """Returns a list of mandatory parameters for IE measurement"""
        return [
            "potentiostat_mode",
            "amplitude",
            "potential",
            "lower_frequency_limit",
            "start_frequency",
            "upper_frequency_limit",
            "lower_number_of_periods",
            "lower_steps_per_decade",
            "upper_number_of_periods",
            "upper_steps_per_decade",
            "scan_direction",
            "scan_strategy",
            "output_path",
            "naming",
        ]

    def _start_measurements(self):
        self.wr_connection.enablePotentiostat()
        self.wr_connection.measureEIS()
        self.wr_connection.disablePotentiostat()


class BaseManualMeasurements(BaseMeasurement, ABC):
    """
    Base class for manual measurements
    """

    def __init__(self, wr_connection: ThalesRemoteScriptWrapper, measurement_id: str, **kwargs):
        super().__init__(wr_connection, measurement_id, **kwargs)

    def _save_data(self):
        logger.info(f"Saving {self.measurement_name} data to {self._output_filename}.csv")
        write_dict_to_csv(self.measured_data, os.path.join(self.output_path, self._output_filename + '.csv'))

    def run(self):
        super().run()
        self._save_data()


class OpenCircuitPotential(BaseManualMeasurements):
    """
    Open Circuit Potential measurement class. This class is used to measure the open circuit potential of the sample.
    It is a manually implemented measurement. For more information on implementation please refer _start_measurements
    method.
    """
    _measurement_name = 'ocp'

    def __str__(self):
        return 'Open Circuit Potential'

    @property
    def parameters(self):
        """Returns a list of mandatory parameters for OCP measurement"""
        return [
            'current',
            'delta',
            'output_path',
            'potentiostat_mode',
            'seconds',
        ]

    def _send_parameters(self):
        self.wr_connection.setPotentiostatMode(self.potentiostat_mode)
        self.wr_connection.setCurrent(self.current)

    @safe_pot
    def _start_measurements(self):
        measured_data = {'time': [], 'potential_V': []}
        for i in range(0, self.seconds, self.delta):
            potential = self.wr_connection.getPotential()
            logger.info(f'Second:\t{i}\tPotential:\t{potential}V')
            measured_data['time'].append(i)
            measured_data['potential_V'].append(potential)
            time.sleep(self.delta)
        self.measured_data = measured_data
        return True


class Impedance(BaseManualMeasurements):
    """
    This class is used to measure impedance of a cell. It is a manually implemented measurement. For more information
    on implementation please refer _start_measurements method.
    """
    _measurement_name = 'imp'

    def __str__(self):
        return 'Impedance'

    @property
    def parameters(self):
        return [
            'amplitude',
            'current',
            'delta',
            'frequency',
            'number_of_periods',
            'output_path',
            'potentiostat_mode',
            'seconds',
        ]

    def _send_parameters(self):
        self.wr_connection.setPotentiostatMode(self.potentiostat_mode)
        self.wr_connection.setCurrent(self.current)

    @safe_pot
    def _start_measurements(self):
        """
        Start measurements for Impedance measurement
        """
        measured_data = {'time': [], 'impedance_Ohm': [], 'phase_deg': []}
        for i in range(0, self.seconds, self.delta):
            response = self.wr_connection.getImpedance(
                frequency=self.frequency,
                amplitude=self.amplitude,
                number_of_periods=self.number_of_periods)

            imp = float(response.real)
            phase = float(response.imag)
            measured_data['time'].append(i)
            measured_data['impedance_Ohm'].append(imp)
            measured_data['phase_deg'].append(phase)
            logger.info(f'Seconds:\t{i}\tImpedance:\t {imp} Ohm\tPhase:\t{phase}°')
            time.sleep(self.delta)
        self.measured_data = measured_data
        return True


class ChronoAmperometry(BaseManualMeasurements):
    """
    This class will perform a chronoamperometry measurement.
    """
    _measurement_name = 'ca'

    def __str__(self):
        return 'Chronoamperometry'

    @property
    def parameters(self):
        return [
            'induction_pot',
            'induction_t',
            'electrolysis_pot',
            'electrolysis_t',
            'relaxation_pot',
            'relaxation_t',
            'sample_rate',
            'potentiostat_mode',
            'output_path',
        ]

    def _send_parameters(self):
        self.wr_connection.setPotentiostatMode(self.potentiostat_mode)

    def _set_induction(self):
        self.wr_connection.setPotential(self.induction_pot)

    def _set_electrolysis(self):
        self.wr_connection.setPotential(self.electrolysis_pot)

    def _set_relaxation(self):
        self.wr_connection.setPotential(self.relaxation_pot)

    @safe_pot
    def _start_measurements(self):
        measured_data = {'time': [], 'current_A': []}
        # induction phase
        logger.info(f'Induction phase for {self.induction_t} seconds with {self.induction_pot} V')
        self._set_induction()
        time.sleep(self.induction_t)

        # electrolysis phase
        logger.info(f'Electrolysis phase for {self.electrolysis_t} seconds with {self.electrolysis_pot} V')
        start_time = datetime.now().timestamp()  # get start phase time
        self._set_electrolysis()
        while (datetime.now().timestamp() - start_time) < self.electrolysis_t:
            current = self.wr_connection.getCurrent()
            seconds = datetime.now().timestamp() - start_time
            measured_data['time'].append(seconds)
            measured_data['current_A'].append(current)
            logger.info(f'Seconds:\t{seconds}\tCurrent:\t {current} A')
            time.sleep(1 / self.sample_rate)  # if sample rate 0.5 will wait 2 seconds between samples

        # relaxation phase
        logger.info(f'Relaxation phase for {self.relaxation_t} seconds with {self.relaxation_pot} V')
        self._set_relaxation()
        time.sleep(self.relaxation_t)

        self.measured_data = measured_data
