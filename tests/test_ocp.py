from unittest import mock

import pytest

from autothalix.measurements import OpenCircuitPotential


@pytest.fixture
def ocp_measurement(mocker: mock):
    """Create a mock instance of OpenCircuitPotential with mocked `wr_connection`"""
    wr_connection = mocker.MagicMock()
    wr_connection.getPotential.return_value = 1.1
    ocp_measurement = OpenCircuitPotential(wr_connection, 'test_ocp')
    return ocp_measurement


def test_measurement_name(ocp_measurement):
    """Test the measurement name"""
    assert ocp_measurement.measurement_name == 'ocp'


def test_parameters(ocp_measurement):
    """Test the parameters"""
    assert ocp_measurement.parameters == [
        'current',
        'delta',
        'output_path',
        'potentiostat_mode',
        'seconds',
    ]


def test_send_parameters(ocp_measurement):
    """Test the parameters are sent to the potentiostat"""
    ocp_measurement._send_parameters()
    ocp_measurement.wr_connection.setPotentiostatMode.assert_called_once_with(ocp_measurement.potentiostat_mode)
    ocp_measurement.wr_connection.setCurrent.assert_called_once_with(ocp_measurement.current)


def test_start_measurements_diff_delta(ocp_measurement):
    """Test the measurements are taken at the correct intervals"""
    ocp_measurement.seconds = 4
    ocp_measurement.delta = 2  # 2 seconds
    print(ocp_measurement.seconds, print(ocp_measurement.delta))
    ocp_measurement._start_measurements()
    ocp_measurement.wr_connection.getPotential.call_count == 2


def test_start_measurements(ocp_measurement):
    """Test the measurements are taken at the correct intervals"""
    ocp_measurement.seconds = 6
    print(ocp_measurement.seconds, print(ocp_measurement.delta))
    ocp_measurement._start_measurements()
    ocp_measurement.wr_connection.enablePotentiostat.assert_called_once()
    ocp_measurement.wr_connection.disablePotentiostat.assert_called_once()
    ocp_measurement.wr_connection.getPotential.call_count == 6


def test_start_measurements_results_2_sec(ocp_measurement):
    """Test the process of the measurements"""
    ocp_measurement.seconds = 4
    ocp_measurement.delta = 2  # 2 seconds
    ocp_measurement._start_measurements()
    print(ocp_measurement.seconds, print(ocp_measurement.delta))
    ocp_measurement._start_measurements()
    assert len(ocp_measurement.measured_data) == 2
    for i in range(2):
        assert ocp_measurement.measured_data["potential_V"][i] == 1.1
        assert ocp_measurement.measured_data["time"][i] == i * 2


def test_start_measurements_results_1_sec(ocp_measurement):
    """Test the process of the measurements"""
    ocp_measurement.seconds = 4
    ocp_measurement.delta = 1  # 2 seconds
    ocp_measurement._start_measurements()
    print(ocp_measurement.seconds, print(ocp_measurement.delta))
    ocp_measurement._start_measurements()
    assert len(ocp_measurement.measured_data["potential_V"]) == 4
    assert len(ocp_measurement.measured_data["time"]) == 4
    for i in range(0, 4):
        assert ocp_measurement.measured_data["potential_V"][i] == 1.1
        assert ocp_measurement.measured_data["time"][i] == i
