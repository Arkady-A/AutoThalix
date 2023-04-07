from unittest import mock

import pytest
from thales_remote.script_wrapper import ThalesRemoteScriptWrapper

from autothalix.measurements import Impedance


@pytest.fixture
def imp_measurement(mocker: mock):
    """Create a mock instance of Impedance with mocked `wr_connection`"""
    # create a mock instance of OpenCircuitPotential with mocked `wr_connection`
    wr_connection = mocker.MagicMock()  # type: ThalesRemoteScriptWrapper
    wr_connection.getImpedance.return_value = 1.1
    imp_measurement = Impedance(wr_connection, 'test_ocp')
    return imp_measurement


def test_measurement_name(imp_measurement):
    """Test if the measurement name is correct"""
    assert imp_measurement.measurement_name == 'imp'


def test_parameters(imp_measurement):
    """Test if the parameters are correct"""
    assert imp_measurement.parameters == [
        'amplitude',
        'current',
        'delta',
        'frequency',
        'number_of_periods',
        'output_path',
        'potentiostat_mode',
        'seconds',
    ]


def test_send_parameters(imp_measurement):
    """Test if the parameters are sent correctly"""
    imp_measurement._send_parameters()
    imp_measurement.wr_connection.setPotentiostatMode.assert_called_once_with(imp_measurement.potentiostat_mode)
    imp_measurement.wr_connection.setCurrent.assert_called_once_with(imp_measurement.current)


def test_start_measurements_diff_delta(imp_measurement):
    """Test if the measurements are started correctly"""
    imp_measurement.seconds = 4
    imp_measurement.delta = 2  # 2 seconds
    imp_measurement._start_measurements()
    imp_measurement.wr_connection.getImpedance.call_count == 2


def test_start_measurements_diff(imp_measurement):
    """Test if the measurements are started correctly"""
    imp_measurement.seconds = 4
    imp_measurement.delta = 1  # 1 seconds
    imp_measurement._start_measurements()
    imp_measurement.wr_connection.getImpedance.call_count == 4


def test_start_measurements_results_2_sec(imp_measurement):
    """Test if the process of the measurements is correct"""
    imp_measurement.seconds = 4
    imp_measurement.delta = 2  # 2 seconds
    imp_measurement._start_measurements()
    imp_measurement.wr_connection.getImpedance.return_value = complex(3.9, 23)
    imp_measurement._start_measurements()
    assert len(imp_measurement.measured_data["impedance_Ohm"]) == 2
    assert len(imp_measurement.measured_data["phase_deg"]) == 2
    assert len(imp_measurement.measured_data["time"]) == 2
    for i in range(0, 2):
        assert imp_measurement.measured_data["impedance_Ohm"][i] == 3.9
        assert imp_measurement.measured_data["phase_deg"][i] == 23
        assert imp_measurement.measured_data["time"][i] == i * 2


def test_start_measurements_results_1_sec(imp_measurement):
    """Test if the process of the measurements is correct"""
    imp_measurement.seconds = 4
    imp_measurement.delta = 1  # 2 seconds
    imp_measurement.wr_connection.getImpedance.return_value = complex(2.1, 20)
    imp_measurement._start_measurements()
    assert len(imp_measurement.measured_data["impedance_Ohm"]) == 4
    assert len(imp_measurement.measured_data["phase_deg"]) == 4
    assert len(imp_measurement.measured_data["time"]) == 4
    for i in range(0, 4):
        assert imp_measurement.measured_data["impedance_Ohm"][i] == 2.1
        assert imp_measurement.measured_data["phase_deg"][i] == 20
        assert imp_measurement.measured_data["time"][i] == i
