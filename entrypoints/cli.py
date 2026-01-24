#!/usr/bin/env python3
"""
CLI entrypoint for administrative tasks.

Provides commands for:
- Creating admin users
- Setting up infrastructure (DynamoDB tables, S3 buckets)
"""
import asyncio
from datetime import date
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from src.infrastructure.container import Container
from src.application.dtos import CreateAdminDTO

app = typer.Typer(
    name="servidor-cli",
    help="Servidor CLI for administrative tasks",
    add_completion=False
)
console = Console()


@app.command()
def create_admin(
    email: str = typer.Option(..., "--email", "-e", help="Admin email address"),
    password: str = typer.Option(..., "--password", "-p", help="Admin password"),
    name: str = typer.Option(..., "--name", "-n", help="Admin full name"),
    phone: str = typer.Option(..., "--phone", help="Admin phone number"),
    date_of_birth: str = typer.Option(..., "--dob", help="Date of birth (YYYY-MM-DD)"),
    nickname: Optional[str] = typer.Option(None, "--nickname", help="Admin nickname"),
):
    """
    Create a new admin user.
    
    Example:
        python -m entrypoints.cli create-admin \\
            --email admin@example.com \\
            --password SecureP@ss123 \\
            --name "John Admin" \\
            --phone "11999999999" \\
            --dob "1990-01-01"
    """
    console.print("\n[bold cyan]Creating Admin User[/bold cyan]\n")
    
    try:
        # Parse date of birth
        dob = date.fromisoformat(date_of_birth)
        
        # Create DTO
        admin_data = CreateAdminDTO(
            email=email,
            password=password,
            name=name,
            phone=phone,
            date_of_birth=dob,
            nickname=nickname
        )
        
        # Initialize container and get use case
        container = Container()
        admin_use_case = container.admin_use_case()
        
        # Create admin
        admin = asyncio.run(admin_use_case.create_admin(admin_data))
        
        # Display success message
        console.print("[green]✓[/green] Admin user created successfully!\n")
        
        # Display admin details
        table = Table(title="Admin Details")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("ID", str(admin.id))
        table.add_row("Email", admin.email)
        table.add_row("Name", admin.name)
        table.add_row("Phone", admin.phone)
        table.add_row("User Type", admin.user_type.value)
        table.add_row("Active", "Yes" if admin.is_active else "No")
        
        console.print(table)
        console.print("\n[yellow]⚠ Keep these credentials secure![/yellow]\n")
        
    except ValueError as e:
        console.print(f"[red]✗ Error:[/red] {str(e)}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[red]✗ Unexpected error:[/red] {str(e)}")
        raise typer.Exit(code=1)


@app.command()
def create_infra(
    tables: bool = typer.Option(True, "--tables/--no-tables", help="Create DynamoDB tables"),
    buckets: bool = typer.Option(True, "--buckets/--no-buckets", help="Create S3 buckets"),
):
    """
    Create infrastructure resources (DynamoDB tables, S3 buckets).
    
    Example:
        python -m entrypoints.cli create-infra
        python -m entrypoints.cli create-infra --no-buckets
    """
    console.print("\n[bold cyan]Creating Infrastructure[/bold cyan]\n")
    
    try:
        from src.infrastructure.services import InfrastructureService
        
        service = InfrastructureService()
        
        # Create DynamoDB tables
        if tables:
            console.print("[bold]Creating DynamoDB Tables...[/bold]")
            results = service.create_dynamodb_tables()
            
            for table_name, status in results.items():
                if "Created" in status:
                    console.print(f"  [green]✓[/green] {status}")
                elif "Already exists" in status:
                    console.print(f"  [yellow]⚠[/yellow] {status}")
                else:
                    console.print(f"  [red]✗[/red] {status}")
            
            console.print()
        
        # Create S3 buckets
        if buckets:
            console.print("[bold]Creating S3 Buckets...[/bold]")
            results = service.create_s3_buckets()
            
            for bucket_name, status in results.items():
                if "Created" in status:
                    console.print(f"  [green]✓[/green] {status}")
                elif "Already exists" in status:
                    console.print(f"  [yellow]⚠[/yellow] {status}")
                else:
                    console.print(f"  [red]✗[/red] {status}")
            
            console.print()
        
        # List resources
        console.print("[bold]Current Resources:[/bold]")
        
        if tables:
            table_list = service.list_tables()
            console.print(f"  Tables: {', '.join(table_list) if table_list else 'None'}")
        
        if buckets:
            bucket_list = service.list_buckets()
            console.print(f"  Buckets: {', '.join(bucket_list) if bucket_list else 'None'}")
        
        console.print("\n[green]✓ Infrastructure setup complete![/green]\n")
        
    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {str(e)}")
        raise typer.Exit(code=1)


@app.command()
def list_admins():
    """
    List all admin users.
    
    Example:
        python -m entrypoints.cli list-admins
    """
    console.print("\n[bold cyan]Admin Users[/bold cyan]\n")
    
    try:
        container = Container()
        admin_use_case = container.admin_use_case()
        
        admins = asyncio.run(admin_use_case.get_all_admins())
        
        if not admins:
            console.print("[yellow]No admin users found.[/yellow]\n")
            return
        
        table = Table()
        table.add_column("ID", style="cyan")
        table.add_column("Email", style="white")
        table.add_column("Name", style="white")
        table.add_column("Active", style="green")
        
        for admin in admins:
            table.add_row(
                str(admin.id)[:8] + "...",
                admin.email,
                admin.name,
                "Yes" if admin.is_active else "No"
            )
        
        console.print(table)
        console.print(f"\n[bold]Total:[/bold] {len(admins)} admin(s)\n")
        
    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {str(e)}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
