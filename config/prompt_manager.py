import yaml
import random
from pathlib import Path

class PromptManager:
    def __init__(self, config_path: str = None):
        """Initialize the PromptManager with a path to the prompts config file.
        
        Args:
            config_path (str, optional): Path to the YAML config file. 
                Defaults to 'config/prompts.yaml' in the same directory.
        """
        if config_path is None:
            config_path = Path(__file__).parent / 'prompts.yaml'
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
    
    def generate_prompt(self) -> str:
        """Generate a complete prompt by combining base components with a random activity.
        
        Returns:
            str: The complete prompt for image generation.
        """
        base = self.config['base_prompt']
        activity = random.choice(self.config['activities'])
        
        # Combine the components into a coherent prompt
        prompt = (
            f"{base['subject']} {base['modification']}, {activity}. "
            f"{base['integration']}. {base['posture']}."
        )
        
        return prompt
