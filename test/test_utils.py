import mock
import aiounittest

from leonidas import utils, course


class TestUtils(aiounittest.AsyncTestCase):
    def test_find_email_found(self):
        msg = "Hello, my email is test@alumni.ubc.ca"
        expected = 'test@alumni.ubc.ca'
        actual = utils.find_email(msg)
        self.assertEqual(actual, expected)

    def test_find_email_none(self):
        msg = "Hello, what is an email?"
        actual = utils.find_email(msg)
        self.assertIsNone(actual)

    @mock.patch('leonidas.course.Course._validate')
    async def test_find_courses_found_space(self, _validate_mock):
        msg = "Please add me to CPSC 110"
        expected = {course.Course('CPSC', '110')}
        actual = {c async for c in utils.find_courses(msg)}
        self.assertSetEqual(actual, expected)

    @mock.patch('leonidas.course.Course._validate')
    async def test_find_courses_found_no_space(self, _validate_mock):
        msg = "FISH506G 101"
        expected = {course.Course('FISH', '506G', '101')}
        actual = {c async for c in utils.find_courses(msg)}
        self.assertSetEqual(actual, expected)

    @mock.patch('leonidas.course.Course._validate')
    async def test_find_courses_found_no_space_at_all(self, _validate_mock):
        msg = "CPSC415101"
        expected = {course.Course('CPSC', '415', '101')}
        actual = {c async for c in utils.find_courses(msg)}
        self.assertSetEqual(actual, expected)


    @mock.patch('leonidas.course.Course._validate')
    async def test_find_courses_section(self, _validate_mock):
        msg = "Please add me to CPSC 110 101"
        expected = {course.Course('CPSC', '110', section='101')}
        actual = {c async for c in utils.find_courses(msg)}
        self.assertSetEqual(actual, expected)

    @mock.patch('leonidas.course.Course._validate')
    async def test_find_courses_section(self, _validate_mock):
        msg = "AFST 351A-001"
        expected = {course.Course('AFST', '351A', section='001')}
        actual = {c async for c in utils.find_courses(msg)}
        self.assertSetEqual(actual, expected)

    @mock.patch('leonidas.course.Course._validate')
    async def test_find_courses_empty(self, _validate_mock):
        msg = "I hate squirrels"
        actual = {c async for c in utils.find_courses(msg)}
        self.assertSetEqual(actual, set())

    async def test_find_courses_invalid_course(self):
        msg = "I would like to be added to ALND 110 201"
        actual = {c async for c in utils.find_courses(msg)}
        self.assertSetEqual(actual, {"ALND 110 201"})


