from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import yaml
import os

@dataclass
class DeploymentConfig:
    name: str
    environment: str
    created_at: datetime
    updated_at: datetime
    config_data: Dict
    status: str

class DeploymentService:
    def __init__(self, config_dir: str = "deployments"):
        self.config_dir = config_dir
        self.active_deployments: Dict[str, DeploymentConfig] = {}
        os.makedirs(config_dir, exist_ok=True)

    def create_deployment(self, name: str, environment: str, config_data: Dict) -> DeploymentConfig:
        """Create a new deployment configuration"""
        if name in self.active_deployments:
            raise ValueError(f"Deployment {name} already exists")

        deployment = DeploymentConfig(
            name=name,
            environment=environment,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            config_data=config_data,
            status="created"
        )

        self.active_deployments[name] = deployment
        self._save_config(deployment)
        return deployment

    def update_deployment(self, name: str, config_data: Dict) -> DeploymentConfig:
        """Update an existing deployment configuration"""
        if name not in self.active_deployments:
            raise ValueError(f"Deployment {name} does not exist")

        deployment = self.active_deployments[name]
        deployment.config_data.update(config_data)
        deployment.updated_at = datetime.now()
        deployment.status = "updated"

        self._save_config(deployment)
        return deployment

    def delete_deployment(self, name: str) -> None:
        """Delete a deployment configuration"""
        if name not in self.active_deployments:
            return

        config_path = os.path.join(self.config_dir, f"{name}.yaml")
        if os.path.exists(config_path):
            os.remove(config_path)

        del self.active_deployments[name]

    def get_deployment(self, name: str) -> Optional[DeploymentConfig]:
        """Get a specific deployment configuration"""
        return self.active_deployments.get(name)

    def list_deployments(self) -> List[Dict]:
        """List all deployment configurations"""
        return [
            {
                "name": deployment.name,
                "environment": deployment.environment,
                "created_at": deployment.created_at.isoformat(),
                "updated_at": deployment.updated_at.isoformat(),
                "status": deployment.status
            }
            for deployment in self.active_deployments.values()
        ]

    def _save_config(self, deployment: DeploymentConfig) -> None:
        """Save deployment configuration to file"""
        config_data = {
            "name": deployment.name,
            "environment": deployment.environment,
            "created_at": deployment.created_at.isoformat(),
            "updated_at": deployment.updated_at.isoformat(),
            "config": deployment.config_data,
            "status": deployment.status
        }

        config_path = os.path.join(self.config_dir, f"{deployment.name}.yaml")
        with open(config_path, "w") as f:
            yaml.dump(config_data, f)

    def _load_configs(self) -> None:
        """Load all deployment configurations from files"""
        if not os.path.exists(self.config_dir):
            return

        for filename in os.listdir(self.config_dir):
            if filename.endswith(".yaml"):
                config_path = os.path.join(self.config_dir, filename)
                with open(config_path, "r") as f:
                    config_data = yaml.safe_load(f)

                deployment = DeploymentConfig(
                    name=config_data["name"],
                    environment=config_data["environment"],
                    created_at=datetime.fromisoformat(config_data["created_at"]),
                    updated_at=datetime.fromisoformat(config_data["updated_at"]),
                    config_data=config_data["config"],
                    status=config_data["status"]
                )
                self.active_deployments[deployment.name] = deployment