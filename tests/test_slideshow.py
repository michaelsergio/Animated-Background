class SlideshowTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_creating_xml(self):
        test_files = [
        'Aurora Over Raufarhöfn [798 x 1200].jpg',
        'NGC 3314 A &amp; B photographed by Hubble [3276x2928] .jpg',
        'Northern Star Lights over Grand Tetons - GTNP [1600 x 1067] [OC].jpg',
        ]

        SRC_DIR = '/home/sergio/.redditbackgrounds'
        image_files = [os.path.join(SRC_DIR, image_file) for image_file in test_files]

        make_xml(image_files).write(sys.stdout, encoding="utf-8")
