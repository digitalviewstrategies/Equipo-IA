"""
Meta Ads MCP Server — Digital View

Wraps MetaAdsAPI from scripts/meta_api.py as an MCP server.
Run: python3 agentes/04_pauta/mcp_server/meta_ads_mcp.py

Requires: pip install mcp
Credentials: reads from agentes/04_pauta/.env
"""

import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load credentials from 04_pauta/.env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# Add scripts/ to path so we can import MetaAdsAPI
scripts_path = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_path))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

server = Server("meta-ads-dv")

TOOLS = [
    types.Tool(
        name="get_campaigns",
        description="Lista campañas de un ad account. Devuelve id, name, status, objective.",
        inputSchema={
            "type": "object",
            "properties": {
                "ad_account_id": {
                    "type": "string",
                    "description": "ID del ad account con prefijo act_ (ej: act_123456789)"
                },
                "status": {
                    "type": "string",
                    "enum": ["ACTIVE", "PAUSED", "ALL"],
                    "description": "Filtro de status. Default: ACTIVE"
                }
            },
            "required": ["ad_account_id"]
        }
    ),
    types.Tool(
        name="get_insights",
        description="Obtiene métricas de performance de un ad account o campaña específica.",
        inputSchema={
            "type": "object",
            "properties": {
                "ad_account_id": {
                    "type": "string",
                    "description": "ID del ad account con prefijo act_"
                },
                "date_preset": {
                    "type": "string",
                    "enum": ["last_7d", "last_14d", "last_30d", "this_month", "last_month"],
                    "description": "Período de análisis"
                },
                "campaign_id": {
                    "type": "string",
                    "description": "ID de campaña específica (opcional, si se omite trae todas)"
                },
                "level": {
                    "type": "string",
                    "enum": ["account", "campaign", "adset", "ad"],
                    "description": "Nivel de granularidad. Default: ad"
                }
            },
            "required": ["ad_account_id", "date_preset"]
        }
    ),
    types.Tool(
        name="update_budget",
        description="Actualiza el presupuesto diario de un ad set.",
        inputSchema={
            "type": "object",
            "properties": {
                "ad_set_id": {
                    "type": "string",
                    "description": "ID del ad set"
                },
                "daily_budget_cents": {
                    "type": "integer",
                    "description": "Nuevo presupuesto diario en centavos de USD (ej: 5000 = USD 50)"
                }
            },
            "required": ["ad_set_id", "daily_budget_cents"]
        }
    ),
    types.Tool(
        name="pause_ad",
        description="Pausa un anuncio específico.",
        inputSchema={
            "type": "object",
            "properties": {
                "ad_id": {
                    "type": "string",
                    "description": "ID del ad a pausar"
                }
            },
            "required": ["ad_id"]
        }
    ),
    types.Tool(
        name="create_campaign",
        description="Crea una campaña nueva con estructura básica. special_ad_categories vacio por default.",
        inputSchema={
            "type": "object",
            "properties": {
                "ad_account_id": {
                    "type": "string",
                    "description": "ID del ad account con prefijo act_"
                },
                "name": {
                    "type": "string",
                    "description": "Nombre de la campaña. Seguir naming: [CLIENTE]_[OBJETIVO]_[YYYY-MM]"
                },
                "objective": {
                    "type": "string",
                    "enum": ["OUTCOME_LEADS", "OUTCOME_TRAFFIC", "OUTCOME_SALES"],
                    "description": "Objetivo de la campaña. Default para DV: OUTCOME_LEADS"
                }
            },
            "required": ["ad_account_id", "name", "objective"]
        }
    )
]


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    try:
        from meta_api import MetaAdsAPI
    except ImportError:
        return [types.TextContent(
            type="text",
            text="Error: no se pudo importar MetaAdsAPI. Verificá que scripts/meta_api.py existe."
        )]

    try:
        if name == "get_campaigns":
            api = MetaAdsAPI(ad_account_id=arguments["ad_account_id"])
            status = arguments.get("status", "ACTIVE")
            result = api.get_campaigns(status=status)
            return [types.TextContent(type="text", text=str(result))]

        elif name == "get_insights":
            api = MetaAdsAPI(ad_account_id=arguments["ad_account_id"])
            campaign_id = arguments.get("campaign_id")
            level = arguments.get("level", "ad")
            result = api.get_insights(
                campaign_id=campaign_id,
                date_preset=arguments["date_preset"],
                level=level
            )
            return [types.TextContent(type="text", text=str(result))]

        elif name == "update_budget":
            api = MetaAdsAPI()
            result = api.update_ad_set_budget(
                ad_set_id=arguments["ad_set_id"],
                daily_budget=arguments["daily_budget_cents"]
            )
            return [types.TextContent(type="text", text=str(result))]

        elif name == "pause_ad":
            api = MetaAdsAPI()
            result = api.pause_ad(ad_id=arguments["ad_id"])
            return [types.TextContent(type="text", text=str(result))]

        elif name == "create_campaign":
            api = MetaAdsAPI(ad_account_id=arguments["ad_account_id"])
            result = api.create_campaign(
                name=arguments["name"],
                objective=arguments["objective"],
                special_ad_categories=[]
            )
            return [types.TextContent(type="text", text=str(result))]

        else:
            return [types.TextContent(type="text", text=f"Tool desconocida: {name}")]

    except Exception as e:
        return [types.TextContent(type="text", text=f"Error al ejecutar {name}: {str(e)}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
