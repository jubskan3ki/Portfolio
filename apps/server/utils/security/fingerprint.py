"""Device fingerprinting pour identification des appareils."""

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

from utils.network import get_client_ip


@dataclass
class DeviceFingerprint:
    """Represente l'empreinte d'un appareil.

    Note: Les champs accept_language, accept_encoding et platform sont stockes
    pour information et affichage, mais ne sont PAS utilises dans le hash car
    ils peuvent varier entre les requetes d'un meme navigateur, ce qui causerait
    des echecs d'authentification. Seul le user_agent est utilise pour le hash.
    """

    ip_address: str
    user_agent: str
    accept_language: str = ""
    accept_encoding: str = ""
    platform: str = ""
    fingerprint_hash: str = field(default="", init=False)

    def __post_init__(self):
        """Genere le hash de l'empreinte apres initialisation."""
        self.fingerprint_hash = self._generate_hash()

    def _generate_hash(self) -> str:
        """Genere un hash unique base sur les caracteristiques stables de l'appareil.

        Utilise User-Agent et Accept-Language (partie principale) pour renforcer
        le fingerprint tout en restant stable entre les requetes d'un meme navigateur.
        """
        # Extraire la langue principale (ex: "fr" de "fr-FR,fr;q=0.9,en;q=0.8")
        primary_lang = ""
        if self.accept_language:
            primary_lang = self.accept_language.split(",", maxsplit=1)[0]
            primary_lang = primary_lang.split(";", maxsplit=1)[0].strip()
        data = {
            "ua": self.user_agent,
            "lang": primary_lang,
        }
        fingerprint_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(fingerprint_str.encode()).hexdigest()[:32]

    def to_dict(self) -> dict[str, Any]:
        """Convertit en dictionnaire."""
        return {
            "ip_address": self.ip_address,
            "user_agent": self.user_agent[:255] if self.user_agent else "",
            "accept_language": self.accept_language[:50] if self.accept_language else "",
            "platform": self.platform[:50] if self.platform else "",
            "fingerprint_hash": self.fingerprint_hash,
        }

    @property
    def browser(self) -> str:
        """Extrait le navigateur du user agent."""
        ua = self.user_agent.lower()
        if "firefox" in ua:
            return "Firefox"
        if "chrome" in ua and "edg" not in ua:
            return "Chrome"
        if "safari" in ua and "chrome" not in ua:
            return "Safari"
        if "edg" in ua:
            return "Edge"
        if "opera" in ua or "opr" in ua:
            return "Opera"
        return "Unknown"

    @property
    def os(self) -> str:
        """Extrait le systeme d'exploitation du user agent."""
        ua = self.user_agent.lower()
        if "windows" in ua:
            return "Windows"
        if "mac os" in ua or "macos" in ua:
            return "macOS"
        if "linux" in ua:
            return "Linux"
        if "android" in ua:
            return "Android"
        if "iphone" in ua or "ipad" in ua:
            return "iOS"
        return "Unknown"

    @property
    def is_mobile(self) -> bool:
        """Detecte si l'appareil est mobile."""
        ua = self.user_agent.lower()
        mobile_keywords = ["mobile", "android", "iphone", "ipad", "ipod", "tablet"]
        return any(kw in ua for kw in mobile_keywords)


def generate_fingerprint(request: Any) -> DeviceFingerprint:
    """Genere une empreinte a partir d'une requete HTTP."""
    return DeviceFingerprint(
        ip_address=get_client_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
        accept_language=request.META.get("HTTP_ACCEPT_LANGUAGE", ""),
        accept_encoding=request.META.get("HTTP_ACCEPT_ENCODING", ""),
        platform=request.META.get("HTTP_SEC_CH_UA_PLATFORM", ""),
    )


def extract_device_info(request: Any) -> dict[str, Any]:
    """Extrait les informations de l'appareil d'une requete."""
    fingerprint = generate_fingerprint(request)
    return {
        **fingerprint.to_dict(),
        "browser": fingerprint.browser,
        "os": fingerprint.os,
        "is_mobile": fingerprint.is_mobile,
    }
