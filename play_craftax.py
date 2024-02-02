import pygame

import jax
import jax.numpy as jnp
import numpy as np

from craftax.constants import (
    OBS_DIM,
    BLOCK_PIXEL_SIZE_HUMAN,
    INVENTORY_OBS_HEIGHT,
    Action,
    Achievement,
    BlockType,
)
from craftax.envs.craftax_symbolic_env import CraftaxEnv
from craftax.renderer import render_craftax_pixels


class CraftaxRenderer:
    def __init__(self, env: CraftaxEnv, env_params, pixel_render_size=4):
        self.env = env
        self.env_params = env_params
        self.pixel_render_size = pixel_render_size
        self.pygame_events = []

        self.screen_size = (
            OBS_DIM[1] * BLOCK_PIXEL_SIZE_HUMAN * pixel_render_size,
            (OBS_DIM[0] + INVENTORY_OBS_HEIGHT)
            * BLOCK_PIXEL_SIZE_HUMAN
            * pixel_render_size,
        )

        # Init rendering
        pygame.init()

        self.screen_surface = pygame.display.set_mode(self.screen_size)

        self._render = jax.jit(render_craftax_pixels, static_argnums=(1,))

    def render(self, env_state):
        # Update pygame events
        self.pygame_events = list(pygame.event.get())

        # Clear
        self.screen_surface.fill((0, 0, 0))

        pixels = self._render(env_state, block_pixel_size=BLOCK_PIXEL_SIZE_HUMAN)
        pixels = jnp.repeat(pixels, repeats=self.pixel_render_size, axis=0)
        pixels = jnp.repeat(pixels, repeats=self.pixel_render_size, axis=1)

        surface = pygame.surfarray.make_surface(np.array(pixels).transpose((1, 0, 2)))
        self.screen_surface.blit(surface, (0, 0))

        # Update screen
        pygame.display.flip()
        # time.sleep(0.01)

    def is_quit_requested(self):
        for event in self.pygame_events:
            if event.type == pygame.QUIT:
                return True
        return False

    def get_action_from_keypress(self, state):
        if state.is_sleeping or state.is_resting:
            return Action.NOOP.value
        for event in self.pygame_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return Action.NOOP.value
                if event.key == pygame.K_w:
                    return Action.UP.value
                elif event.key == pygame.K_d:
                    return Action.RIGHT.value
                elif event.key == pygame.K_s:
                    return Action.DOWN.value
                elif event.key == pygame.K_a:
                    return Action.LEFT.value
                elif event.key == pygame.K_SPACE:
                    return Action.DO.value
                elif event.key == pygame.K_1:
                    return Action.MAKE_WOOD_PICKAXE.value
                elif event.key == pygame.K_t:
                    return Action.PLACE_TABLE.value
                elif event.key == pygame.K_TAB:
                    return Action.SLEEP.value
                elif event.key == pygame.K_r:
                    return Action.PLACE_STONE.value
                elif event.key == pygame.K_f:
                    return Action.PLACE_FURNACE.value
                elif event.key == pygame.K_p:
                    return Action.PLACE_PLANT.value
                elif event.key == pygame.K_2:
                    return Action.MAKE_STONE_PICKAXE.value
                elif event.key == pygame.K_3:
                    return Action.MAKE_IRON_PICKAXE.value
                elif event.key == pygame.K_4:
                    return Action.MAKE_DIAMOND_PICKAXE.value
                elif event.key == pygame.K_5:
                    return Action.MAKE_WOOD_SWORD.value
                elif event.key == pygame.K_6:
                    return Action.MAKE_STONE_SWORD.value
                elif event.key == pygame.K_7:
                    return Action.MAKE_IRON_SWORD.value
                elif event.key == pygame.K_8:
                    return Action.MAKE_DIAMOND_SWORD.value
                elif event.key == pygame.K_e:
                    return Action.REST.value
                elif event.key == pygame.K_COMMA:
                    return Action.ASCEND.value
                elif event.key == pygame.K_PERIOD:
                    return Action.DESCEND.value
                elif event.key == pygame.K_y:
                    return Action.MAKE_IRON_ARMOUR.value
                elif event.key == pygame.K_u:
                    return Action.MAKE_DIAMOND_ARMOUR.value
                elif event.key == pygame.K_i:
                    return Action.SHOOT_ARROW.value
                elif event.key == pygame.K_o:
                    return Action.MAKE_ARROW.value
                elif event.key == pygame.K_g:
                    return Action.CAST_FIREBALL.value
                elif event.key == pygame.K_h:
                    return Action.CAST_ICEBALL.value
                elif event.key == pygame.K_j:
                    return Action.PLACE_TORCH.value
                elif event.key == pygame.K_z:
                    return Action.DRINK_POTION_RED.value
                elif event.key == pygame.K_x:
                    return Action.DRINK_POTION_GREEN.value
                elif event.key == pygame.K_c:
                    return Action.DRINK_POTION_BLUE.value
                elif event.key == pygame.K_v:
                    return Action.DRINK_POTION_PINK.value
                elif event.key == pygame.K_b:
                    return Action.DRINK_POTION_CYAN.value
                elif event.key == pygame.K_n:
                    return Action.DRINK_POTION_YELLOW.value
                elif event.key == pygame.K_m:
                    return Action.READ_BOOK.value
                elif event.key == pygame.K_k:
                    return Action.ENCHANT_SWORD.value
                elif event.key == pygame.K_l:
                    return Action.ENCHANT_ARMOUR.value
                elif event.key == pygame.K_LEFTBRACKET:
                    return Action.MAKE_TORCH.value
                elif event.key == pygame.K_RIGHTBRACKET:
                    return Action.LEVEL_UP_DEXTERITY.value
                elif event.key == pygame.K_MINUS:
                    return Action.LEVEL_UP_STRENGTH.value
                elif event.key == pygame.K_EQUALS:
                    return Action.LEVEL_UP_INTELLIGENCE.value

        return None


def print_new_achievements(old_achievements, new_achievements):
    for i in range(len(old_achievements)):
        if old_achievements[i] == 0 and new_achievements[i] == 1:
            print(
                f"{Achievement(i).name} ({new_achievements.sum()}/{len(Achievement)})"
            )


def print_symbolic_obs(obs, map_obs_shape):
    flat_map_obs_shape = map_obs_shape[0] * map_obs_shape[1] * map_obs_shape[2]
    image_obs = obs[:flat_map_obs_shape]
    image_obs = image_obs.reshape(map_obs_shape)
    flat_obs = obs[flat_map_obs_shape:]

    block_map = image_obs[:, :, : len(BlockType)].argmax(axis=-1)
    mob_map = image_obs[:, :, len(BlockType) : -1].argmax(axis=-1)
    light_map = image_obs[:, :, -1]


def main():
    env = CraftaxEnv(CraftaxEnv.default_static_params())
    env_params = env.default_params

    rng = jax.random.PRNGKey(np.random.randint(2**31))
    rng, _rng = jax.random.split(rng)
    obs, env_state = env.reset(_rng, env_params)

    pixel_render_size = 4

    renderer = CraftaxRenderer(env, env_params, pixel_render_size=pixel_render_size)

    step_fn = jax.jit(env.step)

    while not renderer.is_quit_requested():
        action = renderer.get_action_from_keypress(env_state)

        if action is not None:
            rng, _rng = jax.random.split(rng)
            old_achievements = env_state.achievements
            print_symbolic_obs(obs, env.get_map_obs_shape())
            obs, env_state, reward, done, info = step_fn(
                _rng, env_state, action, env_params
            )
            new_achievements = env_state.achievements
            print_new_achievements(old_achievements, new_achievements)

            if done:
                obs, env_state = env.reset(_rng, env_params)
                print(new_achievements)

            if reward > 0.8:
                print(f"Reward: {reward}\n")

        renderer.render(env_state)


if __name__ == "__main__":
    debug = False
    if debug:
        with jax.disable_jit():
            main()
    else:
        main()
