"""
meta_api.py — Wrapper de Meta Marketing API para DV Media Buyer.

Maneja la creacion, edicion y consulta de campanas, ad sets, ads e insights
via la Graph API de Meta (v21.0).

Requiere .env en la raiz de 04_pauta/ con:
    META_ACCESS_TOKEN=tu_token
    META_BUSINESS_ID=1394099734579403

El ad_account_id es por cliente y se lee del brand system
(shared/brands/[cliente].json bajo meta_ads.ad_account_id).
Se pasa al constructor al instanciar el cliente por cada operacion.
"""

import json
import os
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

# Cargar .env desde la raiz del agente
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(ENV_PATH)

API_VERSION = "v21.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"


class MetaAPIError(Exception):
    """Error de la Meta Marketing API con contexto."""

    def __init__(self, message: str, response: dict | None = None):
        self.response = response
        super().__init__(message)


class MetaAdsAPI:
    """Cliente para Meta Marketing API.

    Para operaciones a nivel de cuenta (crear campana, subir imagen, listar
    ads, etc) hay que pasar ad_account_id al constructor. Para operaciones
    a nivel business (listar cuentas accesibles, validar token) no hace falta.
    """

    def __init__(
        self,
        access_token: str | None = None,
        ad_account_id: str | None = None,
        business_id: str | None = None,
    ):
        self.access_token = access_token or os.getenv("META_ACCESS_TOKEN")
        self.ad_account_id = ad_account_id
        self.business_id = business_id or os.getenv("META_BUSINESS_ID")

        if not self.access_token:
            raise MetaAPIError(
                "META_ACCESS_TOKEN no configurado. "
                "Crea un archivo .env en la raiz de 04_pauta/ con tu token."
            )

    def _require_account(self) -> str:
        """Valida que haya ad_account_id configurado para la operacion."""
        if not self.ad_account_id:
            raise MetaAPIError(
                "Esta operacion requiere ad_account_id. "
                "Instancia MetaAdsAPI(ad_account_id=...) desde el brand del cliente."
            )
        return self.ad_account_id

    def _require_business(self) -> str:
        """Valida que haya business_id configurado para la operacion."""
        if not self.business_id:
            raise MetaAPIError(
                "Esta operacion requiere business_id. "
                "Configura META_BUSINESS_ID en .env o pasalo al constructor."
            )
        return self.business_id

    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
        data: dict | None = None,
    ) -> dict:
        """Ejecuta un request a la Graph API."""
        url = f"{BASE_URL}/{endpoint}"
        params = params or {}
        params["access_token"] = self.access_token

        try:
            resp = requests.request(method, url, params=params, json=data, timeout=30)
            result = resp.json()
        except requests.exceptions.Timeout:
            raise MetaAPIError("Timeout al conectar con Meta API. Reintenta.")
        except requests.exceptions.RequestException as e:
            raise MetaAPIError(f"Error de conexion: {e}")

        if "error" in result:
            error = result["error"]
            code = error.get("code", "")
            msg = error.get("message", "Error desconocido")

            if code == 190:
                raise MetaAPIError(
                    f"Token expirado o invalido. Renova el token en Meta Business Manager. "
                    f"Detalle: {msg}",
                    result,
                )
            if code == 17:
                raise MetaAPIError(
                    f"Rate limit alcanzado. Espera unos minutos. Detalle: {msg}",
                    result,
                )

            raise MetaAPIError(f"Error Meta API ({code}): {msg}", result)

        return result

    # --- Campaigns ---

    def create_campaign(
        self,
        name: str,
        objective: str,
        status: str = "PAUSED",
        special_ad_categories: list[str] | None = None,
        is_adset_budget_sharing_enabled: bool = True,
        bid_strategy: str = "LOWEST_COST_WITHOUT_CAP",
    ) -> dict:
        """
        Crea una campana.

        Args:
            name: nombre siguiendo naming convention DV.
            objective: OUTCOME_LEADS, OUTCOME_TRAFFIC, OUTCOME_SALES.
            status: PAUSED (default, para revisar antes de activar) o ACTIVE.
            special_ad_categories: lista vacia por default. No se declara HOUSING
                salvo que Felipe lo pida explicitamente.
            is_adset_budget_sharing_enabled: True = ABO (presupuesto por ad set).
            bid_strategy: LOWEST_COST_WITHOUT_CAP por default.
        """
        if special_ad_categories is None:
            special_ad_categories = []

        params = {
            "name": name,
            "objective": objective,
            "status": status,
            "special_ad_categories": json.dumps(special_ad_categories),
            "is_adset_budget_sharing_enabled": is_adset_budget_sharing_enabled,
            "bid_strategy": bid_strategy,
        }

        return self._request("POST", f"{self._require_account()}/campaigns", params=params)

    def list_campaigns(self, status_filter: str | None = None) -> list[dict]:
        """Lista campanas de la cuenta."""
        params = {
            "fields": "id,name,objective,status,daily_budget,lifetime_budget",
        }
        if status_filter:
            params["effective_status"] = json.dumps([status_filter])

        result = self._request("GET", f"{self._require_account()}/campaigns", params=params)
        return result.get("data", [])

    def update_campaign(self, campaign_id: str, **kwargs) -> dict:
        """Actualiza campos de una campana (name, status, etc)."""
        return self._request("POST", campaign_id, params=kwargs)

    # --- Ad Sets ---

    def create_ad_set(
        self,
        campaign_id: str,
        name: str,
        targeting: dict,
        daily_budget: int,
        optimization_goal: str = "LEAD_GENERATION",
        billing_event: str = "IMPRESSIONS",
        status: str = "PAUSED",
        start_time: str | None = None,
        placements: dict | None = None,
    ) -> dict:
        """
        Crea un ad set.

        Args:
            campaign_id: ID de la campana padre.
            name: nombre siguiendo naming convention DV.
            targeting: dict de targeting (geo, edad, intereses, exclusiones).
            daily_budget: presupuesto diario en centavos (ej: 500 = USD 5.00).
            optimization_goal: LEAD_GENERATION, LINK_CLICKS, LANDING_PAGE_VIEWS.
            billing_event: IMPRESSIONS (default).
            status: PAUSED o ACTIVE.
            start_time: ISO 8601 datetime string.
            placements: dict de publisher_platforms y positions.
        """
        params = {
            "campaign_id": campaign_id,
            "name": name,
            "targeting": json.dumps(targeting),
            "daily_budget": daily_budget,
            "optimization_goal": optimization_goal,
            "billing_event": billing_event,
            "status": status,
        }

        if start_time:
            params["start_time"] = start_time

        if placements:
            # Merge placements into targeting
            tgt = json.loads(params["targeting"])
            tgt.update(placements)
            params["targeting"] = json.dumps(tgt)

        return self._request("POST", f"{self._require_account()}/adsets", params=params)

    def list_ad_sets(self, campaign_id: str) -> list[dict]:
        """Lista ad sets de una campana."""
        params = {
            "fields": "id,name,status,daily_budget,targeting,optimization_goal",
        }
        result = self._request("GET", f"{campaign_id}/adsets", params=params)
        return result.get("data", [])

    def update_ad_set(self, ad_set_id: str, **kwargs) -> dict:
        """Actualiza campos de un ad set (budget, status, targeting, etc)."""
        return self._request("POST", ad_set_id, params=kwargs)

    # --- Ads ---

    def create_ad(
        self,
        ad_set_id: str,
        name: str,
        creative_id: str,
        status: str = "PAUSED",
    ) -> dict:
        """
        Crea un ad usando un creative existente.

        Args:
            ad_set_id: ID del ad set padre.
            name: nombre siguiendo naming convention DV.
            creative_id: ID del ad creative en la cuenta.
            status: PAUSED o ACTIVE.
        """
        params = {
            "adset_id": ad_set_id,
            "name": name,
            "creative": json.dumps({"creative_id": creative_id}),
            "status": status,
        }

        return self._request("POST", f"{self._require_account()}/ads", params=params)

    def create_ad_with_creative(
        self,
        ad_set_id: str,
        name: str,
        creative_spec: dict,
        status: str = "PAUSED",
    ) -> dict:
        """
        Crea un ad con un creative inline (sin creative_id previo).

        Args:
            creative_spec: dict con object_story_spec, link_data, etc.
        """
        params = {
            "adset_id": ad_set_id,
            "name": name,
            "creative": json.dumps(creative_spec),
            "status": status,
        }

        return self._request("POST", f"{self._require_account()}/ads", params=params)

    def list_ads(self, ad_set_id: str) -> list[dict]:
        """Lista ads de un ad set."""
        params = {
            "fields": "id,name,status,creative",
        }
        result = self._request("GET", f"{ad_set_id}/ads", params=params)
        return result.get("data", [])

    def update_ad(self, ad_id: str, **kwargs) -> dict:
        """Actualiza campos de un ad (status, name, etc)."""
        return self._request("POST", ad_id, params=kwargs)

    # --- Creative & Images ---

    def upload_image(self, image_path: str) -> dict:
        """
        Sube una imagen a la libreria de la cuenta.

        Returns:
            Dict con 'hash' e 'url' de la imagen.
        """
        url = f"{BASE_URL}/{self._require_account()}/adimages"

        with open(image_path, "rb") as img:
            files = {"filename": img}
            params = {"access_token": self.access_token}
            resp = requests.post(url, params=params, files=files, timeout=60)
            result = resp.json()

        if "error" in result:
            raise MetaAPIError(
                f"Error subiendo imagen: {result['error'].get('message', 'desconocido')}",
                result,
            )

        # El response tiene la imagen bajo images -> {filename} -> hash
        images = result.get("images", {})
        if images:
            img_data = next(iter(images.values()))
            return {"hash": img_data.get("hash"), "url": img_data.get("url", "")}

        return result

    def upload_video(self, video_path: str, title: str = "") -> dict:
        """
        Sube un video a la libreria de la cuenta.

        Returns:
            Dict con 'id' del video.
        """
        url = f"{BASE_URL}/{self._require_account()}/advideos"

        with open(video_path, "rb") as vid:
            files = {"source": vid}
            params = {"access_token": self.access_token, "title": title}
            resp = requests.post(url, params=params, files=files, timeout=300)
            result = resp.json()

        if "error" in result:
            raise MetaAPIError(
                f"Error subiendo video: {result['error'].get('message', 'desconocido')}",
                result,
            )

        return result

    # --- Insights ---

    def get_insights(
        self,
        object_id: str,
        date_range: dict | None = None,
        fields: list[str] | None = None,
        breakdowns: list[str] | None = None,
        level: str | None = None,
        time_increment: int | str | None = None,
    ) -> list[dict]:
        """
        Obtiene metricas de performance.

        Args:
            object_id: ID de campaign, ad set, o ad.
            date_range: {"since": "YYYY-MM-DD", "until": "YYYY-MM-DD"}.
            fields: lista de campos (ver metricas_benchmarks.md).
            breakdowns: ["publisher_platform", "platform_position"], etc.
            level: "campaign", "adset", "ad" para desglosar.
            time_increment: 1 (diario), 7 (semanal), "monthly", "all_days".
        """
        if fields is None:
            fields = [
                "campaign_name", "adset_name", "ad_name",
                "spend", "impressions", "reach", "frequency",
                "clicks", "ctr", "cpc", "cpm",
                "actions", "cost_per_action_type",
                "video_p25_watched_actions", "video_p50_watched_actions",
                "video_p75_watched_actions", "video_p100_watched_actions",
                "video_play_actions",
            ]

        params: dict[str, Any] = {"fields": ",".join(fields)}

        if date_range:
            params["time_range"] = json.dumps(date_range)
        if breakdowns:
            params["breakdowns"] = ",".join(breakdowns)
        if level:
            params["level"] = level
        if time_increment:
            params["time_increment"] = time_increment

        result = self._request("GET", f"{object_id}/insights", params=params)
        return result.get("data", [])

    # --- Status ---

    def update_status(self, object_id: str, status: str) -> dict:
        """Cambia el status de cualquier objeto (campaign, ad set, ad)."""
        return self._request("POST", object_id, params={"status": status})

    def pause(self, object_id: str) -> dict:
        """Pausa un objeto."""
        return self.update_status(object_id, "PAUSED")

    def activate(self, object_id: str) -> dict:
        """Activa un objeto."""
        return self.update_status(object_id, "ACTIVE")

    # --- Budget ---

    def update_budget(self, ad_set_id: str, daily_budget: int) -> dict:
        """
        Actualiza el presupuesto diario de un ad set.

        Args:
            daily_budget: en centavos (ej: 500 = USD 5.00).
        """
        return self._request(
            "POST", ad_set_id, params={"daily_budget": daily_budget}
        )

    # --- Business level ---

    def list_ad_accounts(self, include_client: bool = True) -> list[dict]:
        """
        Lista todas las ad accounts accesibles desde el business portfolio.

        Args:
            include_client: si True, incluye client_ad_accounts ademas de owned.

        Returns:
            Lista de dicts con id, name, account_status, currency, kind ("owned" | "client").
        """
        business_id = self._require_business()
        fields = "id,name,account_status,currency"

        owned = self._request(
            "GET", f"{business_id}/owned_ad_accounts",
            params={"fields": fields, "limit": 100},
        ).get("data", [])
        for acc in owned:
            acc["kind"] = "owned"

        if not include_client:
            return owned

        client = self._request(
            "GET", f"{business_id}/client_ad_accounts",
            params={"fields": fields, "limit": 100},
        ).get("data", [])
        for acc in client:
            acc["kind"] = "client"

        return owned + client

    def get_account_info(self) -> dict:
        """Info de la ad account actualmente configurada."""
        return self._request(
            "GET", self._require_account(),
            params={"fields": "id,name,account_status,currency,timezone_name,business"},
        )
