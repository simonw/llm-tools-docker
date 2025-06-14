import llm
import subprocess
import os
import json
from typing import Optional


class DockerAlpine(llm.Toolbox):
    _container_id: Optional[str] = None

    def _get_container_id(self) -> str:
        if not self._container_id:
            self._start_container()
        return self._container_id

    def _start_container(self):
        """Start an Alpine Linux container with current directory mounted."""
        current_dir = os.getcwd()
        
        try:
            # Start container in detached mode with current directory mounted
            result = subprocess.run([
                'docker', 'run', '-d', '--rm',
                '-v', f'{current_dir}:/workspace',
                '-w', '/workspace',
                'alpine:latest',
                'tail', '-f', '/dev/null'  # Keep container running
            ], capture_output=True, text=True, check=True)
            
            self._container_id = result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to start Docker container: {e.stderr}")

    def execute_command(self, command: str) -> str:
        """
        Execute a command in the Alpine Linux container.
        The current directory is mounted as /workspace in the container.
        
        Examples:
        - ls -la
        - cat /etc/os-release
        - apk add --no-cache python3
        - python3 --version
        """
        container_id = self._get_container_id()
        
        try:
            result = subprocess.run([
                'docker', 'exec', container_id, 'sh', '-c', command
            ], capture_output=True, text=True, timeout=30)
            
            output = result.stdout
            if result.stderr:
                output += f"\nSTDERR: {result.stderr}"
            if result.returncode != 0:
                output += f"\nReturn code: {result.returncode}"
                
            return output
        except subprocess.TimeoutExpired:
            return "Error: Command timed out after 30 seconds"
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {e.stderr}"

    def stop_container(self):
        """Stop and remove the Alpine container."""
        if self._container_id:
            try:
                subprocess.run(['docker', 'stop', self._container_id], 
                             capture_output=True, check=True)
                self._container_id = None
            except subprocess.CalledProcessError:
                pass  # Container might already be stopped

    def container_info(self) -> str:
        """Get information about the running container."""
        if not self._container_id:
            return "No container running"
        
        try:
            result = subprocess.run([
                'docker', 'inspect', self._container_id
            ], capture_output=True, text=True, check=True)
            
            info = json.loads(result.stdout)[0]
            return f"Container ID: {self._container_id}\nStatus: {info['State']['Status']}\nImage: {info['Config']['Image']}"
        except Exception as e:
            return f"Error getting container info: {str(e)}"


def docker_alpine(command: str) -> str:
    """
    Execute a command in an Alpine Linux container with the current directory mounted.
    
    Examples:
    - ls -la
    - cat /etc/os-release  
    - apk add --no-cache curl
    - curl --version
    """
    current_dir = os.getcwd()
    
    try:
        result = subprocess.run([
            'docker', 'run', '--rm',
            '-v', f'{current_dir}:/workspace',
            '-w', '/workspace',
            'alpine:latest',
            'sh', '-c', command
        ], capture_output=True, text=True, timeout=30, check=True)
        
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds"
    except subprocess.CalledProcessError as e:
        return f"Error (exit code {e.returncode}): {e.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"


@llm.hookimpl
def register_tools(register):
    register(DockerAlpine)
    register(docker_alpine)
