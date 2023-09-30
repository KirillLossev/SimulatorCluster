import carla
import random

def spawn_hero(world):
        """Spawns the hero actor when the script runs"""
        # Get a random blueprint.
        blueprint = random.choice(world.get_blueprint_library().filter('vehicle.*'))
        blueprint.set_attribute('role_name', 'hero')
        if blueprint.has_attribute('color'):
            color = random.choice(blueprint.get_attribute('color').recommended_values)
            blueprint.set_attribute('color', color)
        # Spawn the player.
        hero_actor = None
        while hero_actor is None:
            spawn_points = world.get_map().get_spawn_points()
            spawn_point = random.choice(spawn_points) if spawn_points else carla.Transform()
            hero_actor = world.try_spawn_actor(blueprint, spawn_point)

        return hero_actor

def select_hero_actor(world):
        """Selects only one hero actor if there are more than one. If there are not any, it will spawn one."""
        hero_vehicles = [actor for actor in world.get_actors()
                         if 'vehicle' in actor.type_id and actor.attributes['role_name'] == 'hero']
        if len(hero_vehicles) > 0:
            return hero_vehicles[0]
        else:
            return spawn_hero(world)