from unittest import mock

import pytest

from autothalix.measurements import ChronoAmperometry


@pytest.fixture
def ca_measurement(mocker: mock):
    """Create a mock instance of OpenCircuitPotential with mocked `wr_connection`"""
    wr_connection = mocker.MagicMock()
    wr_connection.getPotential.return_value = 1.1
    ca_measurement = ChronoAmperometry(wr_connection, 'test_ocp')
    return ca_measurement


def test_measurement_name(ca_measurement):
    """Test the measurement name"""
    assert ca_measurement.measurement_name == 'ca'


def test_parameters(ca_measurement):
    """Test the parameters"""
    assert ca_measurement.parameters ==  [
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


def test_send_parameters(ca_measurement):
    """Test the parameters are sent to the potentiostat"""
    ca_measurement._send_parameters()
    ca_measurement.wr_connection.setPotentiostatMode.assert_called_once_with(ca_measurement.potentiostat_mode)


def test_phases(ca_measurement):
    """Test that every phase called"""
    ca_measurement._start_measurements()
    ca_measurement.wr_connection.enablePotentiostat.assert_called_once()
    ca_measurement.wr_connection.disablePotentiostat.assert_called_once()
    ca_measurement.wr_connection.getPotential.call_count == 3 # 3 phases = 3 calls

