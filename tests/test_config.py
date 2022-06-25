"""Script to test the config module of the PhysiCOOL package."""
import unittest
from shutil import copyfile
from xml.etree import ElementTree

from physicool import config
from physicool import pcxml
import physicool.datatypes as dt
from configdata import *


class PhysiCellConfigTest(unittest.TestCase):
    def setUp(self):
        """Creates and stores a parser object to read data from the config file."""
        copyfile(CONFIG_PATH, WRITE_PATH)
        self.xml_data = config.ConfigFileParser(CONFIG_PATH)
        self.xml_write = config.ConfigFileParser(WRITE_PATH)

    def test_get_cell_definition_list(self):
        """Asserts that the cell definitions extracted from the config file are correct."""
        cell_list = self.xml_data.cell_definitions_list
        self.assertEqual(cell_list, ["default", "cancer"])

    def test_read_domain_params(self):
        """Asserts that the XML domain data was properly read into a dt.Domain object."""
        expected_data = config.dt.Domain(**EXPECTED_DOMAIN_READ)
        domain_data = self.xml_data.read_domain_params()
        self.assertEqual(expected_data, domain_data)

    def test_read_overall_params(self):
        expected_data = dt.Overall(**EXPECTED_OVERALL_READ)
        overall_data = self.xml_data.read_overall_params()
        self.assertEqual(expected_data, overall_data)

    def test_read_me_params(self):
        expected_data = [dt.Substance(**EXPECTED_SUBSTANCE_READ)]
        me_data = self.xml_data.read_me_params()
        self.assertEqual(expected_data, me_data)

    def test_read_cycle_durations_params(self):
        """Asserts that the volume parameters extracted from the config file are correct."""
        expected_data = dt.Cycle(**EXPECTED_CYCLE_DURATIONS_READ)
        cycle_data = self.xml_data.read_cycle_params("default")
        self.assertEqual(expected_data, cycle_data)

    def test_read_cycle_rates_params(self):
        """Asserts that the volume parameters extracted from the config file are correct."""
        expected_data = dt.Cycle(**EXPECTED_CYCLE_RATES_READ)
        cycle_data = self.xml_data.read_cycle_params("cancer")
        self.assertEqual(expected_data, cycle_data)

    def test_read_death(self):
        expected_data = [
            dt.Death(**EXPECTED_DEATH_APOPTOSIS_READ),
            dt.Death(**EXPECTED_DEATH_NECROSIS_READ),
        ]
        death_data = self.xml_data.read_death_params("default")
        self.assertEqual(expected_data, death_data)

    def test_read_volume_params(self):
        """Asserts that the volume parameters extracted from the config file are correct."""
        expected_data = dt.Volume(**EXPECTED_VOLUME_READ)
        volume_data = self.xml_data.read_volume_params("default")
        self.assertEqual(expected_data, volume_data)

    def test_read_mechanics_params(self):
        """Asserts that the mechanics parameters extracted from the config file are correct."""
        expected_data = dt.Mechanics(**EXPECTED_MECHANICS_READ)
        mechanics_data = self.xml_data.read_mechanics_params("default")
        self.assertEqual(expected_data, mechanics_data)

    def test_read_motility_params(self):
        """Asserts that the motility parameters extracted from the config file are correct."""
        expected_data = dt.Motility(**EXPECTED_MOTILITY_READ)
        motility_data = self.xml_data.read_motility_params("default")
        self.assertEqual(expected_data, motility_data)

    def test_read_secretion_params(self):
        """Asserts that the secretion parameters extracted from the config file are correct."""
        expected_data = [
            dt.Secretion(**EXPECTED_SECRETION_READ_SUBSTRATE),
            dt.Secretion(**EXPECTED_SECRETION_READ_OXYGEN),
        ]
        secretion_data = self.xml_data.read_secretion_params("default")
        self.assertEqual(expected_data, secretion_data)

    def test_read_custom_params(self):
        expected_data = [dt.CustomData(**custom) for custom in EXPECTED_CUSTOM_READ]
        custom_data = self.xml_data.read_custom_data("default")
        self.assertEqual(expected_data, custom_data)

    def test_read_user_parameters(self):
        expected_data = [
            dt.CustomData(**custom) for custom in EXPECTED_USER_PARAMETERS_READ
        ]
        user_data = self.xml_data.read_user_params()
        self.assertEqual(expected_data, user_data)

    def test_write_domain_params(self):
        """Asserts that Domain data is properly written to the XML file."""
        domain_data = self.xml_write.read_domain_params()
        domain_data.x_min = -200.0
        domain_data.x_max = 200.0
        domain_data.use_2d = False
        self.xml_write.write_domain_params(domain=domain_data)

        new_tree = ElementTree.parse(WRITE_PATH)
        domain_data = pcxml.parse_domain(
            tree=new_tree,
            path="domain",
        )
        self.assertEqual(EXPECTED_DOMAIN_WRITE, domain_data)

    def test_write_overall_params(self):
        """Asserts that overall data is properly written to the XML file."""
        overall_data = self.xml_write.read_overall_params()
        overall_data.max_time = 120.0
        self.xml_write.write_overall_params(overall=overall_data)

        new_tree = ElementTree.parse(WRITE_PATH)
        overall_data = pcxml.parse_overall(
            tree=new_tree,
            path="overall",
        )
        self.assertEqual(EXPECTED_OVERALL_WRITE, overall_data)

    def test_write_substance_params(self):
        """Asserts that overall data is properly written to the XML file."""
        substance_data = self.xml_write.read_me_params()
        substance_data[0].diffusion_coefficient = 400.0
        substance_data[0].decay_rate = 1.0
        self.xml_write.write_substance_params(substance=substance_data[0])

        new_tree = ElementTree.parse(WRITE_PATH)
        substance_data = pcxml.parse_substance(
            tree=new_tree, path="microenvironment_setup", name="substrate"
        )
        self.assertEqual(EXPECTED_SUBSTANCE_WRITE, substance_data)

    def test_write_cycle_durations_params(self):
        cycle_data = self.xml_write.read_cycle_params("default")
        cycle_data.phase_durations = [100.0, 10.0, 240.0, 60.0]
        self.xml_write.write_cycle_params(name="default", cycle=cycle_data)

        new_tree = ElementTree.parse(WRITE_PATH)
        cycle_data = pcxml.parse_cycle(
            tree=new_tree,
            path="cell_definitions/cell_definition[@name='default']/phenotype/cycle",
        )
        self.assertEqual(EXPECTED_CYCLE_DURATIONS_WRITE, cycle_data)

    def test_write_cycle_rates_params(self):
        cycle_data = self.xml_write.read_cycle_params("cancer")
        cycle_data.phase_transition_rates = [0.001, 0.001, 0.00416667, 0.0166667]
        self.xml_write.write_cycle_params(name="cancer", cycle=cycle_data)

        new_tree = ElementTree.parse(WRITE_PATH)
        cycle_data = pcxml.parse_cycle(
            tree=new_tree,
            path="cell_definitions/cell_definition[@name='cancer']/phenotype/cycle",
        )
        self.assertEqual(EXPECTED_CYCLE_RATES_WRITE, cycle_data)

    def test_write_death_params(self):
        death_data = self.xml_write.read_death_params("default")
        death_data[0].phase_durations = [518.0]
        death_data[0].calcification_rate = 0.5
        self.xml_write.write_death_model_params(name="default", death=death_data[0], model_name="apoptosis")

        new_tree = ElementTree.parse(WRITE_PATH)
        death_data = pcxml.parse_death_model(
            tree=new_tree,
            path="cell_definitions/cell_definition[@name='default']/phenotype/death",
            name="apoptosis"
        )
        self.assertEqual(EXPECTED_DEATH_APOPTOSIS_WRITE, death_data)

    def test_write_volume_params(self):
        volume_data = self.xml_write.read_volume_params("default")
        volume_data.nuclear = 100.0
        volume_data.calcified_fraction = 0.5
        volume_data.calcification_rate = 1.0
        volume_data.relative_rupture_volume = 3.0
        self.xml_write.write_volume_params(name="default", volume=volume_data)

        new_tree = ElementTree.parse(WRITE_PATH)
        volume_data = pcxml.parse_volume(
            tree=new_tree,
            path="cell_definitions/cell_definition[@name='default']/phenotype/volume",
        )
        self.assertEqual(EXPECTED_VOLUME_WRITE, volume_data)

    def test_write_mechanics_params(self):
        mechanics_data = self.xml_write.read_mechanics_params("default")
        mechanics_data.cell_cell_adhesion_strength = 4.0
        mechanics_data.cell_cell_repulsion_strength = 100.0
        self.xml_write.write_mechanics_params(name="default", mechanics=mechanics_data)

        new_tree = ElementTree.parse(WRITE_PATH)
        mechanics_data = pcxml.parse_mechanics(
            tree=new_tree,
            path="cell_definitions/cell_definition[@name='default']/phenotype/mechanics",
        )
        self.assertEqual(EXPECTED_MECHANICS_WRITE, mechanics_data)

    def test_write_motility_params(self):
        motility_data = self.xml_write.read_motility_params("default")
        motility_data.speed = 12.0
        motility_data.persistence_time = 60.0
        motility_data.motility_enabled = True
        self.xml_write.write_motility_params(name="default", motility=motility_data)

        new_tree = ElementTree.parse(WRITE_PATH)
        motility_data = pcxml.parse_motility(
            tree=new_tree,
            path="cell_definitions/cell_definition[@name='default']/phenotype/motility",
        )
        self.assertEqual(EXPECTED_MOTILITY_WRITE, motility_data)

    def test_write_custom_params(self):
        custom_data = self.xml_write.read_custom_data("default")
        custom_data[0].value = 5.0
        self.xml_write.write_custom_params(name="default", custom_data=custom_data)

        new_tree = ElementTree.parse(WRITE_PATH)
        custom_data = pcxml.parse_custom(
            tree=new_tree,
            path="cell_definitions/cell_definition[@name='default']/custom_data",
        )
        self.assertEqual(EXPECTED_CUSTOM_WRITE, custom_data)

    def test_write_user_params(self):
        custom_data = self.xml_write.read_user_params()
        custom_data[0].value = 1.0
        custom_data[1].value = 5.0
        self.xml_write.write_user_params(custom_data=custom_data)

        new_tree = ElementTree.parse(WRITE_PATH)
        custom_data = pcxml.parse_custom(
            tree=new_tree,
            path="user_parameters",
        )
        self.assertEqual(EXPECTED_USER_PARAMETERS_WRITE, custom_data)

    def tearDown(self) -> None:
        Path(WRITE_PATH).unlink()


if __name__ == "__main__":
    unittest.main()
