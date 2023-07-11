import pytest
from unittest import mock

from autothalix.measurements import ElectrochemicalImpedanceSpectroscopy

@pytest.fixture
def eis_measurement(mocker):
    """Create a mock instance of ElectrochemicalImpedanceSpectroscopy with mocked `wr_connection`"""
    # create a mock instance of ElectrochemicalImpedanceSpectroscopy with mocked `wr_connection`
    wr_connection = mocker.MagicMock()
    eis_measurement = ElectrochemicalImpedanceSpectroscopy(wr_connection, 'test_eis')
    return eis_measurement


def test_param_types(eis_measurement):
    """Test that the parameters are of the correct type."""
    assert isinstance(eis_measurement.amplitude, float)
    assert isinstance(eis_measurement.lower_frequency_limit, float)
    assert isinstance(eis_measurement.lower_number_of_periods, int)
    assert isinstance(eis_measurement.lower_steps_per_decade, float)
    assert isinstance(eis_measurement.naming, str)
    assert isinstance(eis_measurement.output_path, str)
    assert isinstance(eis_measurement.potential, float)
    # assert isinstance(eis_measurement.potentiostat_mode, int)
    assert isinstance(eis_measurement.scan_direction, str)
    assert isinstance(eis_measurement.scan_strategy, str)
    assert isinstance(eis_measurement.start_frequency, float)
    assert isinstance(eis_measurement.upper_frequency_limit, float)
    assert isinstance(eis_measurement.upper_number_of_periods, int)
    assert isinstance(eis_measurement.upper_steps_per_decade, float)


def test_measurement_name(eis_measurement):
    """Test if the measurement name is correct"""
    assert eis_measurement.measurement_name == 'eis'


def test_parameters(eis_measurement):
    """Test if the parameters are correct"""
    assert set(eis_measurement.parameters) == {
        'amplitude',
        'lower_frequency_limit',
        'lower_number_of_periods',
        'lower_steps_per_decade',
        'naming',
        'output_path',
        'potentiostat_mode',
        'potential',
        'scan_direction',
        'scan_strategy',
        'start_frequency',
        'upper_frequency_limit',
        'upper_number_of_periods',
        'upper_steps_per_decade',
    }


def test_send_parameters(eis_measurement):
    """Test if the parameters are sent correctly"""
    eis_measurement._send_parameters()
    eis_measurement.wr_connection.setPotentiostatMode.assert_called_once_with(eis_measurement.potentiostat_mode)
    eis_measurement.wr_connection.setScanStrategy.assert_called_once_with(eis_measurement.scan_strategy)
    eis_measurement.wr_connection.setScanDirection.assert_called_once_with(eis_measurement.scan_direction)
    eis_measurement.wr_connection.setAmplitude.assert_called_once_with(eis_measurement.amplitude)
    eis_measurement.wr_connection.setStartFrequency.assert_called_once_with(eis_measurement.start_frequency)
    eis_measurement.wr_connection.setLowerFrequencyLimit.assert_called_once_with(eis_measurement.lower_frequency_limit)
    eis_measurement.wr_connection.setUpperFrequencyLimit.assert_called_once_with(eis_measurement.upper_frequency_limit)
    eis_measurement.wr_connection.setLowerStepsPerDecade.assert_called_once_with(eis_measurement.lower_steps_per_decade)
    eis_measurement.wr_connection.setUpperStepsPerDecade.assert_called_once_with(eis_measurement.upper_steps_per_decade)
    eis_measurement.wr_connection.setLowerNumberOfPeriods.assert_called_once_with(eis_measurement.lower_number_of_periods)
    eis_measurement.wr_connection.setUpperNumberOfPeriods.assert_called_once_with(eis_measurement.upper_number_of_periods)
    eis_measurement.wr_connection.setPotential.assert_called_once_with(eis_measurement.potential)
    eis_measurement.wr_connection.setEISNaming.assert_called_once_with(eis_measurement.naming)
    eis_measurement.wr_connection.setEISOutputPath.assert_called_once_with(eis_measurement.output_path)

def test_run(eis_measurement):
    """Test that the measurement is run correctly."""
    eis_measurement.run()
    eis_measurement.wr_connection.measureEIS.assert_called_once_with()
