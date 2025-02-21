import os
import sys
import click
import subprocess
from pathlib import Path

@click.group()
def cli():
    """Simba CLI: Manage your Simba application."""
    pass

@cli.command("server")
def run_server():
    """Run the Simba FastAPI server."""
    click.echo("Starting Simba server...")
    # Only import when actually running the server
    from simba.__main__ import create_app
    app = create_app()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=1)

@cli.command("parsers")
def run_parsers():
    """Run the Celery worker for parsing tasks."""
    click.echo("Starting Celery worker for parsing tasks...")
    os.system("celery -A simba.core.celery_config.celery_app worker --loglevel=info -Q parsing")

@cli.command("front")
def run_frontend():
    """Run the React frontend development server."""
    frontend_dir = Path.cwd() / "frontend"
    
    if not frontend_dir.exists():
        click.echo("Error: Frontend directory not found. Please make sure you're in the correct directory.")
        return

    os.chdir(frontend_dir)
    
    # Check if node_modules exists
    if not (frontend_dir / "node_modules").exists():
        click.echo("Installing dependencies...")
        subprocess.run("npm install", shell=True, check=True)
    
    click.echo("Starting React frontend...")
    subprocess.run("npm run dev", shell=True)

@cli.command("help")
def show_help():
    """Show help for Simba CLI."""
    click.echo(cli.get_help(ctx=click.get_current_context()))

def main():
    if len(sys.argv) == 1:
        show_help()
    else:
        cli()

if __name__ == "__main__":
    main() 