from particlesimulation.particles.particle import Particle


class CircleParticle(Particle):
    def __init__(
        self,
        groups,
        pos,
        color,
        speed,
        size,
        fade_speed,
    ):
        super().__init__(
            groups,
            pos,
            color,
            speed,
            size,
            fade_speed,
        )
        self.pos = pos
        self.color = color
        self.size = size
        self.speed = speed
        self.alpha = 255
        self.fade_speed = fade_speed

        self.create_surf()
