from setuptools import setup


setup(name='linguistic_processing',
      version='0.1',
      description="Processes text from a variety of languages. Tokenizes, top words, TFIDF, differential.",
      url='https://github.com/chrisdaly/linguistic_processing',
      author='Chris Daly',
      author_email='chrisdalyyy@gmail.com',
      license='MIT',
      packages=['linguistic_processing'],
      install_requires=["nltk"],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose']
      )
