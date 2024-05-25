# from .craftax_env import make_craftax_env_from_name
import gym
for env in ["Craftax-Symbolic-v1", "Craftax-Pixels-v1", 
            "Craftax-Classic-Symbolic-v1", "Craftax-Classic-Pixels-v1", "Craftax-Symbolic-AutoReset-v1", "Craftax-Pixels-AutoReset-v1", "Craftax-Classic-Symbolic-AutoReset-v1", "Craftax-Classic-Pixels-AutoReset-v1"]:
    gym.register(
        id=env,
        entry_point="craftax.craftax_env:make_craftax_env_from_name",
        kwargs={"name": env},
    )
