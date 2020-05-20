import logging
import os
from abc import ABC, abstractmethod
from PIL import Image, ImageDraw, ImageFilter
from random import randint


class AbstractGenerator(ABC):
    logging.basicConfig(filename="ImageGenerator/logs/gen.log", level=logging.INFO)
    NOISE_FACTOR = 70

    def __init__(self, particles, maxDeltaParticles, radius, maxDeltaRadius, width, height):
        self.particles = particles
        self.maxDeltaParticles = maxDeltaParticles
        self.radius = radius
        self.maxDeltaRadius = maxDeltaRadius

        self.image = None
        self.width = width
        self.height = height

        if not os.path.isdir('ImageGenerator/images'):
            os.mkdir('ImageGenerator/images')

        if not os.path.isdir('ImageGenerator/coordinates'):
            os.mkdir('ImageGenerator/coordinates')

    @abstractmethod
    def generate(self):
        pass

    def createNoise(pix, width, height, idraw, factor):
        for i in range(width):
            for j in range(height):
                rand = randint(-factor, factor)
                a = pix[i, j][0] + rand
                b = pix[i, j][1] + rand
                c = pix[i, j][2] + rand
                if a < 0:
                    a = 0
                if b < 0:
                    b = 0
                if c < 0:
                    c = 0
                if a > 255:
                    a = 255
                if b > 255:
                    b = 255
                if c > 255:
                    c = 255
                idraw.point((i, j), (a, b, c))


class StochasticGenerator(AbstractGenerator):
    imageCounter = 1

    def __init__(self, particles, maxDeltaParticles, radius, maxDeltaRadius, width, height):
        if maxDeltaParticles >= particles or maxDeltaRadius >= radius:
            logging.error("Delta parameters are incorrect")
            logging.info(
                "particles = " + str(particles) + " should be more than maxDeltaParticles = " + str(maxDeltaParticles))
            logging.info("radius = " + str(radius) + " should be more than maxDeltaRadius = " + str(maxDeltaRadius))
            raise ValueError("Delta parameters are not suitable")

        super().__init__(particles, maxDeltaParticles, radius, maxDeltaRadius, width, height)

    def generate(self):
        self.particlesCount = self.particles + randint(-self.maxDeltaParticles, self.maxDeltaParticles)
        self.image = Image.new('RGBA', (self.width, self.height), color='Black')
        idraw = ImageDraw.Draw(self.image)
        file = open('ImageGenerator/coordinates/s' + str(StochasticGenerator.imageCounter) + '.csv', 'w')

        for i in range(self.particlesCount):
            x = randint(0, self.width)
            y = randint(0, self.height)
            currentRadius = randint(self.radius - self.maxDeltaRadius, self.radius + self.maxDeltaRadius)

            upper_left_X = x - currentRadius
            upper_left_Y = y - currentRadius
            bottom_right_X = x + currentRadius
            bottom_right_Y = y + currentRadius

            idraw.ellipse((upper_left_X, upper_left_Y, bottom_right_X, bottom_right_Y),
                          fill="White",
                          outline="Gray")

            if upper_left_X < 0:
                upper_left_X = 0
            if upper_left_Y < 0:
                upper_left_Y = 0
            if bottom_right_X > self.width:
                bottom_right_X = self.width
            if bottom_right_Y > self.height:
                bottom_right_Y = self.height

            file.write(str(upper_left_X) + ',' + str(upper_left_Y) + ',' + str(bottom_right_X) + ',' + str(
                bottom_right_Y) + '\n')

        file.close()
        self.image = self.image.filter(ImageFilter.BLUR)
        pix = self.image.load()
        idraw = ImageDraw.Draw(self.image)
        AbstractGenerator.createNoise(pix, self.width, self.height, idraw, AbstractGenerator.NOISE_FACTOR)
        self.image.save('ImageGenerator/images/s' + str(StochasticGenerator.imageCounter) + '.png', 'PNG')

        StochasticGenerator.imageCounter += 1
