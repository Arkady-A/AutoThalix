from unittest import mock

import pytest

from autothalix.measurements import LinearSweepVoltammetry

@pytest.fixture
def lsv_measurement(mocker):
    """Create a mock instance of LinearSweepVoltammetry with mocked `wr_connection`"""
    # create a mock instance of LinearSweepVoltammetry with mocked `wr_connection`
    wr_connection = mocker.MagicMock()
    lsv_measurement = LinearSweepVoltammetry(wr_connection, 'test_lsv')
    return lsv_measurement


def test_param_types(lsv_measurement):
    """Test that the parameters are of the correct type."""
    assert isinstance(lsv_measurement.absolute_tolerance, float)
    assert isinstance(lsv_measurement.counter, int)
    assert isinstance(lsv_measurement.first_edge_potential, float)
    assert isinstance(lsv_measurement.first_edge_potential_relation, str)
    assert isinstance(lsv_measurement.fourth_edge_potential, float)
    assert isinstance(lsv_measurement.fourth_edge_potential_relation, str)
    assert isinstance(lsv_measurement.maximum_current, float)
    assert isinstance(lsv_measurement.maximum_waiting_time, float)
    assert isinstance(lsv_measurement.minimum_current, float)
    assert isinstance(lsv_measurement.minimum_waiting_time, float)
    assert isinstance(lsv_measurement.naming, str)
    assert isinstance(lsv_measurement.ohmic_drop, float)
    assert isinstance(lsv_measurement.output_path, str)
    assert isinstance(lsv_measurement.potential_resolution, float)
    assert isinstance(lsv_measurement.relative_tolerance, float)
    assert isinstance(lsv_measurement.scan_rate, float)
    assert isinstance(lsv_measurement.second_edge_potential, float)
    assert isinstance(lsv_measurement.second_edge_potential_relation, str)
    assert isinstance(lsv_measurement.sweep_mode, str)
    assert isinstance(lsv_measurement.third_edge_potential, float)
    assert isinstance(lsv_measurement.third_edge_potential_relation, str)

def test_measurement_name(lsv_measurement):
    """Test that the measurement name is correct."""
    assert lsv_measurement.measurement_name == 'lsv'


def test_parameters(lsv_measurement):
    """Test that the parameters are correct."""
    assert set(lsv_measurement.parameters) == {
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
    }


def test_send_parameters(lsv_measurement):
    """Test that the parameters are sent correctly."""
    lsv_measurement._send_parameters()
    lsv_measurement.wr_connection.setIEOutputPath.assert_called_once_with(lsv_measurement.output_path)
    lsv_measurement.wr_connection.setIEOutputFileName.assert_called_once_with(lsv_measurement._output_filename)
    lsv_measurement.wr_connection.setIENaming.assert_called_once_with(lsv_measurement.naming)
    lsv_measurement.wr_connection.setIEScanRate.assert_called_once_with(lsv_measurement.scan_rate)
    lsv_measurement.wr_connection.setIEPotentialResolution.assert_called_once_with(lsv_measurement.potential_resolution)
    lsv_measurement.wr_connection.setIEFirstEdgePotential.assert_called_once_with(lsv_measurement.first_edge_potential)
    lsv_measurement.wr_connection.setIEFirstEdgePotentialRelation.assert_called_once_with(lsv_measurement.first_edge_potential_relation)
    lsv_measurement.wr_connection.setIESecondEdgePotential.assert_called_once_with(lsv_measurement.second_edge_potential)
    lsv_measurement.wr_connection.setIESecondEdgePotentialRelation.assert_called_once_with(lsv_measurement.second_edge_potential_relation)
    lsv_measurement.wr_connection.setIEThirdEdgePotential.assert_called_once_with(lsv_measurement.third_edge_potential)
    lsv_measurement.wr_connection.setIEThirdEdgePotentialRelation.assert_called_once_with(lsv_measurement.third_edge_potential_relation)
    lsv_measurement.wr_connection.setIEFourthEdgePotential.assert_called_once_with(lsv_measurement.fourth_edge_potential)
    lsv_measurement.wr_connection.setIEFourthEdgePotentialRelation.assert_called_once_with(lsv_measurement.fourth_edge_potential_relation)
    lsv_measurement.wr_connection.setIESweepMode.assert_called_once_with(lsv_measurement.sweep_mode)
    lsv_measurement.wr_connection.setIEMinimumCurrent.assert_called_once_with(lsv_measurement.minimum_current)
    lsv_measurement.wr_connection.setIEMaximumCurrent.assert_called_once_with(lsv_measurement.maximum_current)
    lsv_measurement.wr_connection.setIEMinimumWaitingTime.assert_called_once_with(lsv_measurement.minimum_waiting_time)
    lsv_measurement.wr_connection.setIEMaximumWaitingTime.assert_called_once_with(lsv_measurement.maximum_waiting_time)
    lsv_measurement.wr_connection.setIEAbsoluteTolerance.assert_called_once_with(lsv_measurement.absolute_tolerance)
    lsv_measurement.wr_connection.setIERelativeTolerance.assert_called_once_with(lsv_measurement.relative_tolerance)
    lsv_measurement.wr_connection.setIEOhmicDrop.assert_called_once_with(lsv_measurement.ohmic_drop)



def test_run(lsv_measurement):
    """Test that the measurement is run correctly."""
    lsv_measurement.run()
    lsv_measurement.wr_connection.measureIE.assert_called_once_with()