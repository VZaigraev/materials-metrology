import sys
import argparse
from ImageGenerator.Generator import StochasticGenerator


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('count', type=int)
    parser.add_argument('-p', '--particles', default=100, type=int)
    parser.add_argument('-dp', '--deltaParticles', default=0, type=int)
    parser.add_argument('-r', '--radius', default=7, type=int)
    parser.add_argument('-dr', '--deltaRadius', default=0, type=int)
    parser.add_argument('-wi', '--width', default=800, type=int)
    parser.add_argument('-he', '--height', default=600, type=int)
    return parser


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()
    s = StochasticGenerator(namespace.particles, namespace.deltaParticles, namespace.radius, namespace.deltaRadius,
                            namespace.width, namespace.height)
    for _ in range(namespace.count):
        s.generate()
