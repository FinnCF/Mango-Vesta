from setuptools import setup, find_packages

setup(
    name='mango-vesta',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'web3'
        'solana',
        'pandas',
        'numpy',
        'math',
        'eth-typing',
        'etherscan-python'
        'tqdm',
        'moralis',
        'pyth-client-py',
    ],
)