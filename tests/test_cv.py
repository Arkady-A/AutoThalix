import pytest

from autothalix.measurements import CyclicVoltammetry


@pytest.fixture
def cv_measurement(mocker):
    """Create a mock instance of CyclicVoltammetry with mocked `wr_connection`"""
    wr_connection = mocker.MagicMock() # wr_connection is a mock
    cv_measurement = CyclicVoltammetry(wr_connection, 'test_cv') # create a mock instance of CyclicVoltammetry
    return cv_measurement


def test_param_types(cv_measurement):
    """Test that the parameters are of the correct type."""
    assert type(cv_measurement.counter) == int
    assert type(cv_measurement.cycles) == float
    assert type(cv_measurement.end_hold_time) == float
    assert type(cv_measurement.end_potential) == float
    assert type(cv_measurement.lower_reversing_potential) == float
    assert type(cv_measurement.naming) == str
    assert type(cv_measurement.maximum_current) == float
    assert type(cv_measurement.minimum_current) == float
    assert type(cv_measurement.output_path) == str
    assert type(cv_measurement.ohmic_drop) == float
    assert type(cv_measurement.samples_per_cycle) == int
    assert type(cv_measurement.scan_rate) == float
    assert type(cv_measurement.start_hold_time) == float
    assert type(cv_measurement.start_potential) == float
    assert type(cv_measurement.upper_reversing_potential) == float

def test_measurement_name(cv_measurement):
    """Test that the measurement name is correct."""
    assert cv_measurement.measurement_name == 'cv'


def test_parameters(cv_measurement):
    """Test that the parameters are correct."""
    assert set(cv_measurement.parameters) == {'counter', 'cycles', 'end_hold_time', 'end_potential',
                                              'lower_reversing_potential', 'naming', 'maximum_current',
                                              'minimum_current', 'output_path', 'ohmic_drop', 'samples_per_cycle',
                                              'scan_rate', 'start_hold_time', 'start_potential',
                                              'upper_reversing_potential', 'analog_function_generator',
                                              'auto_restart_at_current_overflow', 'auto_restart_at_current_underflow'}


def test_send_parameters(cv_measurement):
    """Test that the parameters are sent correctly."""
    cv_measurement._send_parameters()
    cv_measurement.wr_connection.setCVCounter.assert_called_once_with(cv_measurement.counter)
    cv_measurement.wr_connection.setCVOutputPath.assert_called_once_with(cv_measurement.output_path)
    cv_measurement.wr_connection.setCVOutputFileName.assert_called_once_with(cv_measurement._output_filename)
    cv_measurement.wr_connection.setCVNaming.assert_called_once_with(cv_measurement.naming)
    cv_measurement.wr_connection.setCVStartPotential.assert_called_once_with(cv_measurement.start_potential)
    cv_measurement.wr_connection.setCVUpperReversingPotential.assert_called_once_with(
        cv_measurement.upper_reversing_potential)
    cv_measurement.wr_connection.setCVLowerReversingPotential.assert_called_once_with(
        cv_measurement.lower_reversing_potential)
    cv_measurement.wr_connection.setCVEndPotential.assert_called_once_with(cv_measurement.end_potential)
    cv_measurement.wr_connection.setCVStartHoldTime.assert_called_once_with(cv_measurement.start_hold_time)
    cv_measurement.wr_connection.setCVEndHoldTime.assert_called_once_with(cv_measurement.end_hold_time)
    cv_measurement.wr_connection.setCVCycles.assert_called_once_with(cv_measurement.cycles)
    cv_measurement.wr_connection.setCVSamplesPerCycle.assert_called_once_with(cv_measurement.samples_per_cycle)
    cv_measurement.wr_connection.setCVScanRate.assert_called_once_with(cv_measurement.scan_rate)
    cv_measurement.wr_connection.setCVMaximumCurrent.assert_called_once_with(cv_measurement.maximum_current)
    cv_measurement.wr_connection.setCVMinimumCurrent.assert_called_once_with(cv_measurement.minimum_current)
    cv_measurement.wr_connection.setCVOhmicDrop.assert_called_once_with(cv_measurement.ohmic_drop)


def test_start_measurements(cv_measurement):
    """Test that the measurements are started correctly."""
    cv_measurement._start_measurements()
    cv_measurement.wr_connection.disableCVAutoRestartAtCurrentOverflow.assert_called_once()
    cv_measurement.wr_connection.disableCVAutoRestartAtCurrentUnderflow.assert_called_once()
    cv_measurement.wr_connection.disableCVAnalogFunctionGenerator.assert_called_once()
    cv_measurement.wr_connection.checkCVSetup.assert_called_once()
    cv_measurement.wr_connection.measureCV.assert_called_once()
