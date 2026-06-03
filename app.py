#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import json
import os
import sys
import ssl
import logging
import urllib.request
from datetime import datetime
from pathlib import Path

import aiohttp
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties

from xC4 import (
    GenJoinSquadsPacket, Emote_k, ExiT, GeneRaTePk, CrEaTe_ProTo,
    Ua, EnC_PacKeT, DecodE_HeX
)

from Pb2 import MajoRLoGinrEq_pb2, MajoRLoGinrEs_pb2, PorTs_pb2

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8798038134:AAEUlmP2_75Ps7rTe7WkdOElJXpqGt5Cy9c"
FF_UID = "4812753412"
FF_PASSWORD = "492C6754CD1BB892C11548121956ADF254468453FA0A7A25FA6367F9DF926221"
WEB_PORT = int(os.environ.get("PORT", 8080))

if not BOT_TOKEN or not FF_UID or not FF_PASSWORD:
    logging.error("Missing BOT_TOKEN, FF_UID or FF_PASSWORD")
    sys.exit(1)

online_writer = None
whisper_writer = None
key = None
iv = None
region = None
is_logged_in = False
login_lock = asyncio.Lock()

ITEM_DATA_URL = "https://raw.githubusercontent.com/4737647734/Emote/main/itemData.json"
NAME_TO_ID = {}
ID_TO_NAME = {}

def load_emotes():
    global NAME_TO_ID, ID_TO_NAME
    try:
        with urllib.request.urlopen(ITEM_DATA_URL, timeout=10) as f:
            data = json.load(f)
        for item in data:
            idd = item["Id"]
            name = item["name"].lower()
            NAME_TO_ID[name] = idd
            ID_TO_NAME[idd] = name
        logging.info(f"Loaded {len(data)} emotes")
    except Exception as e:
        logging.error(f"Failed to load emotes: {e}")

load_emotes()

async def GeNeRaTeAccEss(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": await Ua(),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"
    }
    data = {
        "uid": uid, "password": password, "response_type": "token", "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as resp:
            if resp.status != 200:
                return None, None
            data = await resp.json()
            return data.get("open_id"), data.get("access_token")

async def encrypted_proto(encoded_hex):
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad
    cipher = AES.new(b'Yg&tc%DEuh6%Zc^8', AES.MODE_CBC, b'6oyZDr22E3ychjM%')
    return cipher.encrypt(pad(encoded_hex, AES.block_size))

async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = "1.123.1"
    major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    major_login.memory_available.version = 55
    major_login.memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019118695"
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0FUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    string = major_login.SerializeToString()
    return await encrypted_proto(string)

async def MajorLogin(payload):
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    headers = {
        'User-Agent': await Ua(),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Expect': '100-continue',
        'X-Unity-Version': '2018.4.11f1',
        'X-GA': 'v1 1',
        'ReleaseVersion': 'OB53',
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers, ssl=ssl_ctx) as resp:
            return await resp.read() if resp.status == 200 else None

async def DecRypTMajoRLoGin(response):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(response)
    return proto

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': await Ua(),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Expect': '100-continue',
        'X-Unity-Version': '2018.4.11f1',
        'X-GA': 'v1 1',
        'ReleaseVersion': 'OB53',
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers, ssl=ssl_ctx) as resp:
            return await resp.read() if resp.status == 200 else None

async def DecRypTLoGinDaTa(data):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(data)
    return proto

async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9: headers = '0000000'
    elif uid_length == 8: headers = '00000000'
    elif uid_length == 10: headers = '000000'
    elif uid_length == 7: headers = '000000000'
    else: headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"

async def run_tcp_online(ip, port, auth_token):
    global online_writer
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            writer.write(bytes.fromhex(auth_token))
            await writer.drain()
            while True:
                data = await reader.read(4096)
                if not data:
                    break
        except Exception:
            await asyncio.sleep(5)
            online_writer = None

async def run_tcp_chat(ip, port, auth_token, ready, region):
    global whisper_writer
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            writer.write(bytes.fromhex(auth_token))
            await writer.drain()
            ready.set()
            while True:
                data = await reader.read(4096)
                if not data:
                    break
        except Exception:
            await asyncio.sleep(5)
            whisper_writer = None

async def SEndPacKeT(whisper_writer, online_writer, typE, packet):
    if typE == 'OnLine' and online_writer:
        online_writer.write(packet)
        await online_writer.drain()
    elif typE == 'Whisper' and whisper_writer:
        whisper_writer.write(packet)
        await whisper_writer.drain()

async def login_to_freefire():
    global key, iv, region, online_writer, whisper_writer, is_logged_in
    async with login_lock:
        try:
            open_id, access_token = await GeNeRaTeAccEss(FF_UID, FF_PASSWORD)
            if not open_id:
                logging.error("Failed to get open_id")
                return False
            payload = await EncRypTMajoRLoGin(open_id, access_token)
            response = await MajorLogin(payload)
            if not response:
                logging.error("MajorLogin failed")
                return False
            login_res = await DecRypTMajoRLoGin(response)
            url = login_res.url
            region = login_res.region
            token = login_res.token
            bot_uid = login_res.account_uid
            key = login_res.key
            iv = login_res.iv
            timestamp = login_res.timestamp

            login_data = await GetLoginData(url, payload, token)
            if not login_data:
                logging.error("GetLoginData failed")
                return False
            login_dec = await DecRypTLoGinDaTa(login_data)

            online_ip, online_port = login_dec.Online_IP_Port.split(":")
            chat_ip, chat_port = login_dec.AccountIP_Port.split(":")
            auth_token = await xAuThSTarTuP(int(bot_uid), token, int(timestamp), key, iv)

            ready = asyncio.Event()
            asyncio.create_task(run_tcp_chat(chat_ip, int(chat_port), auth_token, ready, region))
            asyncio.create_task(run_tcp_online(online_ip, int(online_port), auth_token))
            await asyncio.wait_for(ready.wait(), timeout=15)
            is_logged_in = True
            logging.info("Logged into Free Fire")
            return True
        except Exception as e:
            logging.error(f"Login error: {e}")
            is_logged_in = False
            return False

async def cmd_dance(team_code, uids, emote_id):
    global is_logged_in, online_writer, whisper_writer, key, iv, region
    if not is_logged_in or online_writer is None:
        return False, "Bot not connected to Free Fire"
    try:
        p = await GenJoinSquadsPacket(team_code, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', p)
        await asyncio.sleep(1.5)
        for uid in uids:
            p = await Emote_k(int(uid), int(emote_id), key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', p)
            await asyncio.sleep(0.4)
        await asyncio.sleep(1)
        p = await ExiT(None, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', p)
        return True, f"Emote {emote_id} sent to {len(uids)} player(s)"
    except Exception as e:
        logging.error(f"Dance error: {e}")
        return False, str(e)

async def periodic_relogin():
    while True:
        await asyncio.sleep(3600)
        logging.info("Periodic re-login...")
        await login_to_freefire()

HTML_PAGE = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>XcTxTeaM EeMoT | مكتبة الإيموجيات</title>
<style>
:root {
  --primary: #ffffff;
  --primary-dark: #cccccc;
  --primary-light: #eeeeee;
  --primary-glow: rgba(255, 255, 255, 0.25);
  --bg-dark: #000000;
  --bg-dark-secondary: #0a0a0a;
  --bg-card: #111111;
  --bg-card-hover: #1c1c1c;
  --text-light: #f5f5f5;
  --text-muted: #999999;
  --text-muted-light: #777777;
  --accent: #ffffff;
  --accent-light: #dddddd;
  --success: #4caf50;
  --error: #f44336;
  --border-radius: 16px;
  --transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  --transition-smooth: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  --shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
  --shadow-hover: 0 16px 48px rgba(0, 0, 0, 0.8);
  --glow: 0 0 30px rgba(255, 255, 255, 0.15);
  --glass-bg: rgba(15, 15, 15, 0.85);
  --glass-border: rgba(255, 255, 255, 0.1);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
  background: var(--bg-dark);
  color: var(--text-light);
  overflow-x: hidden;
  min-height: 100vh;
}
body::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 20% 20%, rgba(255,255,255,0.04) 0%, transparent 50%), radial-gradient(circle at 80% 80%, rgba(255,255,255,0.04) 0%, transparent 50%);
  z-index: -2;
  animation: backgroundFloat 30s ease-in-out infinite alternate;
}
body::after {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, transparent 0%, rgba(255,255,255,0.02) 50%, transparent 100%);
  z-index: -1;
  animation: gradientShift 20s linear infinite;
}
@keyframes backgroundFloat { 0%,100% { transform: translate(0,0) scale(1); } 33% { transform: translate(-1%,1.5%) scale(1.01); } 66% { transform: translate(1.5%,-1%) scale(0.99); } }
@keyframes gradientShift { 0% { transform: translateX(0) translateY(0); } 100% { transform: translateX(100%) translateY(100%); } }
header {
  background: var(--glass-bg);
  backdrop-filter: blur(24px) saturate(180%);
  padding: 16px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: var(--shadow);
  border-bottom: 1px solid var(--glass-border);
  transition: var(--transition-smooth);
  animation: slideDown 0.8s cubic-bezier(0.4,0,0.2,1) both;
}
@keyframes slideDown { from { opacity:0; transform:translateY(-30px); } to { opacity:1; transform:translateY(0); } }
.header-left h1 {
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(135deg, #ffffff, #888888);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.5px;
}
.dropdown { position: relative; }
.dropdown button {
  background: linear-gradient(135deg, #ffffff, #cccccc);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  padding: 10px 20px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: var(--transition-smooth);
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: var(--shadow);
  position: relative;
  overflow: hidden;
}
.dropdown button:hover { transform: translateY(-2px); box-shadow: var(--shadow-hover), var(--glow); }
.dropdown-content {
  display: none;
  position: absolute;
  right: 0;
  top: 100%;
  margin-top: 10px;
  background: var(--glass-bg);
  backdrop-filter: blur(24px);
  min-width: 160px;
  max-height: 350px;
  overflow-y: auto;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-hover);
  border: 1px solid var(--glass-border);
  z-index: 1001;
}
.dropdown-content button {
  background: transparent;
  color: var(--text-light);
  border: none;
  padding: 14px 20px;
  text-align: left;
  width: 100%;
  cursor: pointer;
  border-radius: 0;
  box-shadow: none;
  font-weight: 500;
  justify-content: flex-start;
}
.dropdown-content button:hover { background-color: rgba(255,255,255,0.04); padding-left: 24px; }
.container { padding: 32px; max-width: 1600px; margin: 0 auto; animation: fadeIn 0.8s ease-out 0.2s both; }
@keyframes fadeIn { from { opacity:0; transform:translateY(24px); } to { opacity:1; transform:translateY(0); } }
.input-panel {
  background: var(--glass-bg);
  backdrop-filter: blur(12px);
  border-radius: var(--border-radius);
  padding: 20px;
  margin-bottom: 30px;
  border: 1px solid var(--glass-border);
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-items: flex-start;
  justify-content: center;
}
.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
  min-width: 150px;
}
.input-group label {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--text-muted);
}
.input-group input, .uid-input {
  background: rgba(0,0,0,0.6);
  border: 1px solid var(--glass-border);
  border-radius: 12px;
  padding: 12px 16px;
  color: white;
  font-size: 14px;
  transition: var(--transition);
}
.input-group input:focus, .uid-input:focus { outline: none; border-color: var(--primary); box-shadow: 0 0 15px rgba(255,255,255,0.1); }
.uids-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  flex: 2;
}
.uid-input { flex: 1; min-width: 120px; }
.add-uid-btn {
  background: linear-gradient(135deg, #ffffff, #888888);
  border: none;
  width: 44px;
  height: 44px;
  border-radius: 12px;
  font-size: 24px;
  cursor: pointer;
  transition: var(--transition);
  color: black;
  font-weight: bold;
}
.add-uid-btn:hover { transform: scale(1.05); }
.filters { display: flex; justify-content: center; margin-bottom: 36px; }
.filters input {
  width: 90%;
  max-width: 600px;
  padding: 18px 24px;
  border-radius: var(--border-radius);
  border: 2px solid var(--glass-border);
  background: var(--glass-bg);
  backdrop-filter: blur(12px);
  color: var(--text-light);
  outline: none;
  font-size: 16px;
  transition: var(--transition-smooth);
  box-shadow: var(--shadow);
}
.filters input:focus { border-color: var(--primary); box-shadow: var(--glow), var(--shadow); transform: translateY(-2px); }
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 24px;
  max-height: calc(100vh - 280px);
  overflow-y: auto;
  padding: 16px 8px 32px 0;
}
.grid::-webkit-scrollbar { width: 10px; }
.grid::-webkit-scrollbar-track { background: rgba(255,255,255,0.03); border-radius: 10px; }
.grid::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #ffffff, #888888); border-radius: 10px; }
.card {
  background: var(--bg-card);
  border-radius: var(--border-radius);
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: var(--transition-smooth);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow);
  border: 1px solid var(--glass-border);
}
.card:hover {
  background: var(--bg-card-hover);
  transform: translateY(-8px) scale(1.02);
  box-shadow: var(--shadow-hover), var(--glow);
}
.card img {
  max-width: 90%;
  max-height: 140px;
  object-fit: contain;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.5);
  transition: var(--transition-smooth);
}
.card:hover img { transform: scale(1.08) rotate(1deg); }
.tooltip { font-size: 13px; color: var(--text-muted); margin-top: 14px; font-weight: 600; text-align: center; word-break: break-all; }
.pagination { display: flex; justify-content: center; margin-top: 40px; gap: 8px; }
.pagination button {
  background: var(--glass-bg);
  backdrop-filter: blur(12px);
  color: var(--text-light);
  border: none;
  padding: 12px 20px;
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: var(--transition-smooth);
  font-weight: 600;
  min-width: 48px;
  height: 48px;
  box-shadow: var(--shadow);
  border: 1px solid var(--glass-border);
}
.pagination button.active {
  background: linear-gradient(135deg, #ffffff, #888888);
  color: white;
  box-shadow: var(--glow), var(--shadow);
  transform: scale(1.05);
}
.pagination button:hover:not(.active) { background: rgba(255,255,255,0.05); transform: translateY(-2px); }
.pagination button:disabled { opacity: 0.3; cursor: not-allowed; }
.modal {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.92);
  justify-content: center;
  align-items: center;
  z-index: 2000;
  backdrop-filter: blur(12px);
}
.modal-content {
  background: var(--bg-card);
  padding: 40px;
  border-radius: var(--border-radius);
  max-width: 550px;
  width: 95%;
  text-align: center;
  position: relative;
  box-shadow: var(--shadow-hover);
  border: 1px solid var(--glass-border);
  max-height: 90vh;
  overflow-y: auto;
}
.modal-content img { max-width: 100%; max-height: 320px; object-fit: contain; border-radius: 20px; margin-bottom: 24px; }
.close {
  position: absolute;
  top: 5px;
  right: 5px;
  color: white;
  font-size: 32px;
  cursor: pointer;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: rgba(255,255,255,0.1);
  backdrop-filter: blur(12px);
}
.close:hover { background: rgba(255,255,255,0.2); transform: rotate(90deg) scale(1.1); }
#modalName { font-size: 32px; margin: 0 0 12px; background: linear-gradient(135deg, #ffffff, #888888); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
#modalId { font-size: 18px; margin: 0 0 30px; color: var(--text-muted); padding: 8px 16px; background: rgba(255,255,255,0.05); border-radius: 50px; display: inline-block; }
.toast {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0,0,0,0.9);
  backdrop-filter: blur(20px);
  color: white;
  padding: 12px 24px;
  border-radius: 40px;
  z-index: 2001;
  font-size: 14px;
  pointer-events: none;
  transition: opacity 0.3s;
  opacity: 0;
  border: 1px solid rgba(255,255,255,0.2);
}
.toast.success { background: #2e7d32; }
.toast.error { background: #c62828; }
footer { text-align: center; padding: 30px 20px; color: var(--text-muted); font-size: 13px; border-top: 1px solid var(--glass-border); margin-top: 40px; }
footer a { color: var(--primary-light); text-decoration: none; }
footer a:hover { text-decoration: underline; }
@media (max-width: 768px) { .grid { grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); } .input-panel { flex-direction: column; } }
</style>
</head>
<body>
<header>
  <div class="header-left"><h1>𝕏𝕔𝕋𝕩𝕋𝕖𝕒𝕄 𝔼𝕖𝕄𝕠𝕋</h1></div>
  <div class="header-right">
    <div class="dropdown">
      <button onclick="toggleDropdown()"><span id="dropdownText">OB Update</span> <span id="dropdownArrow">▼</span></button>
      <div id="obDropdown" class="dropdown-content"></div>
    </div>
  </div>
</header>

<div class="container">
  <div class="input-panel">
    <div class="input-group">
      <label>🏷️ Team Code</label>
      <input type="text" id="teamCode" placeholder="مثال: ABC123">
    </div>
    <div class="input-group" style="flex:2">
      <label>👥 Player UIDs</label>
      <div style="display: flex; gap: 8px; flex-wrap: wrap; align-items: center;">
        <div id="uidsContainer" style="display: flex; gap: 8px; flex-wrap: wrap; flex:1">
          <input type="text" class="uid-input" placeholder="UID">
        </div>
        <button class="add-uid-btn" id="addUidBtn">+</button>
      </div>
    </div>
  </div>

  <div class="filters">
    <input type="text" id="searchBox" placeholder="بحث بالاسم أو المعرف (مثال: 909042007)">
  </div>
  <div id="itemsGrid" class="grid">جاري التحميل...</div>
  <div class="pagination" id="pagination"></div>
</div>

<footer>
  <p>XcTxTeaM EeMoT | Developed by <a href="https://t.me/ZikoB0SS" target="_blank">@ZikoB0SS</a></p>
</footer>

<div id="itemModal" class="modal"><div class="modal-content"><span class="close">&times;</span><img id="modalIcon" alt="Emote Preview"><h2 id="modalName"></h2><p id="modalId"></p></div></div>

<script>
const API_URL = "/send_emote";
const ITEM_DATA_URL = "/itemData.json";
const FALLBACK_IMG = "https://via.placeholder.com/100/333333/FFFFFF?text=No+Image";

let allItems = [], selectedOB = "all", currentPage = 1, itemsPerPage = 30;
let ID_TO_NAME = {};

async function fetchData() {
  try {
    const res = await fetch(ITEM_DATA_URL);
    allItems = await res.json();
    allItems.forEach(item => { ID_TO_NAME[item.Id] = item.name; });
    createOBDropdown();
    renderItems();
  } catch(e) { console.error(e); document.getElementById("itemsGrid").innerHTML = "<div>خطأ في تحميل البيانات</div>"; }
}

function createOBDropdown() {
  const dropdown = document.getElementById("obDropdown");
  dropdown.innerHTML = '<button onclick="selectOB(\'all\')">All Updates</button>';
  const versions = new Set();
  allItems.forEach(item => {
    let idStr = item.Id.toString();
    if(idStr.length >= 6) versions.add("OB"+idStr.substring(4,6));
  });
  [...versions].sort((a,b)=>parseInt(b.slice(2))-parseInt(a.slice(2))).forEach(v => {
    let btn = document.createElement("button");
    btn.textContent = v; btn.onclick = () => selectOB(v);
    dropdown.appendChild(btn);
  });
}

function toggleDropdown() {
  let d = document.getElementById("obDropdown");
  d.style.display = d.style.display === "block" ? "none" : "block";
}

function selectOB(ob) {
  selectedOB = ob;
  document.getElementById("dropdownText").innerText = ob === "all" ? "OB Update" : ob;
  currentPage = 1;
  renderItems();
  document.getElementById("obDropdown").style.display = "none";
}

function applyFilters() {
  let search = document.getElementById("searchBox").value.toLowerCase().trim();
  let obCode = selectedOB !== "all" ? selectedOB.slice(2) : null;
  return allItems.filter(item => {
    let idStr = item.Id.toString();
    let matchOB = obCode ? idStr.startsWith("9090"+obCode) : true;
    let matchSearch = !search || item.name.toLowerCase().includes(search) || idStr.includes(search);
    return matchOB && matchSearch;
  });
}

function renderItems() {
  const filtered = applyFilters();
  const grid = document.getElementById("itemsGrid");
  if(filtered.length === 0) {
    grid.innerHTML = "<div style='text-align:center; padding:50px;'>لا توجد إيموجيات</div>";
    updatePagination(0);
    return;
  }
  const start = (currentPage-1)*itemsPerPage;
  const pageItems = filtered.slice(start, start+itemsPerPage);
  grid.innerHTML = "";
  pageItems.forEach((item, idx) => {
    const card = document.createElement("div");
    card.className = "card";
    card.style.animationDelay = `${idx*0.05}s`;
    const imgUrl = `/emote_image/${item.Id}.png`;
    card.innerHTML = `<img src="${imgUrl}" onerror="this.src='${FALLBACK_IMG}'" alt="${item.name}" loading="lazy"><div class="tooltip">${item.Id}</div>`;
    card.onclick = () => sendEmote(item);
    grid.appendChild(card);
  });
  updatePagination(filtered.length);
}

function updatePagination(total) {
  const totalPages = Math.ceil(total / itemsPerPage);
  const pagDiv = document.getElementById("pagination");
  if(totalPages <= 1) { pagDiv.innerHTML = ""; return; }
  pagDiv.innerHTML = "";
  const prevBtn = document.createElement("button");
  prevBtn.innerHTML = "◀";
  prevBtn.disabled = currentPage === 1;
  prevBtn.onclick = () => { if(currentPage > 1) { currentPage--; renderItems(); window.scrollTo({top:0}); } };
  pagDiv.appendChild(prevBtn);
  let startPage = Math.max(1, currentPage-2);
  let endPage = Math.min(totalPages, startPage+4);
  for(let i=startPage; i<=endPage; i++) {
    const btn = document.createElement("button");
    btn.textContent = i;
    if(i === currentPage) btn.classList.add("active");
    btn.onclick = () => { currentPage = i; renderItems(); window.scrollTo({top:0}); };
    pagDiv.appendChild(btn);
  }
  const nextBtn = document.createElement("button");
  nextBtn.innerHTML = "▶";
  nextBtn.disabled = currentPage === totalPages;
  nextBtn.onclick = () => { if(currentPage < totalPages) { currentPage++; renderItems(); window.scrollTo({top:0}); } };
  pagDiv.appendChild(nextBtn);
}

function showToast(msg, isError=false) {
  const toast = document.createElement("div");
  toast.className = `toast ${isError ? "error" : "success"}`;
  toast.innerText = msg;
  document.body.appendChild(toast);
  setTimeout(() => toast.style.opacity = "1", 10);
  setTimeout(() => { toast.style.opacity = "0"; setTimeout(()=>toast.remove(),300); }, 3000);
}

async function sendEmote(item) {
  const teamCode = document.getElementById("teamCode").value.trim();
  const uidInputs = document.querySelectorAll(".uid-input");
  const uids = Array.from(uidInputs).map(inp => inp.value.trim()).filter(v => v && /^\d+$/.test(v));
  if(!teamCode) { showToast("❌ أدخل كود الفريق", true); return; }
  if(uids.length === 0) { showToast("❌ أضف UID واحد على الأقل", true); return; }
  showToast(`⏳ جاري إرسال ${item.name}...`);
  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ team_code: teamCode, uids: uids, emote_id: item.Id })
    });
    const data = await res.json();
    if(data.success) showToast(`✅ ${data.message}`);
    else showToast(`❌ فشل: ${data.message}`, true);
  } catch(e) { showToast("❌ خطأ في الاتصال بالبوت", true); }
}

document.getElementById("addUidBtn").onclick = () => {
  const container = document.getElementById("uidsContainer");
  const newInput = document.createElement("input");
  newInput.type = "text";
  newInput.className = "uid-input";
  newInput.placeholder = "UID";
  container.appendChild(newInput);
};

const modal = document.getElementById("itemModal");
const modalIcon = document.getElementById("modalIcon");
const modalName = document.getElementById("modalName");
const modalId = document.getElementById("modalId");
document.querySelector(".close").onclick = () => { modal.style.display = "none"; document.body.style.overflow = "auto"; };
window.onclick = e => { if(e.target === modal) { modal.style.display = "none"; document.body.style.overflow = "auto"; } if(!e.target.closest('.dropdown')) document.getElementById("obDropdown").style.display = "none"; };
window.addEventListener("load", fetchData);
let searchTimeout;
document.getElementById("searchBox").addEventListener("input", () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => { currentPage = 1; renderItems(); }, 300);
});
</script>
</body>
</html>
"""

async def handle_root(request):
    return web.Response(text=HTML_PAGE, content_type='text/html')

async def handle_item_data(request):
    try:
        with urllib.request.urlopen(ITEM_DATA_URL, timeout=10) as f:
            data = json.load(f)
        return web.json_response(data)
    except Exception as e:
        return web.json_response([], status=500)

async def handle_emote_image(request):
    image_id = request.match_info.get('id')
    if not image_id:
        return web.Response(status=404)
    image_url = f"https://raw.githubusercontent.com/4737647734/Emote/main/emote_image/{image_id}.png"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                if resp.status == 200:
                    img_data = await resp.read()
                    return web.Response(body=img_data, content_type='image/png')
                else:
                    return web.Response(status=404)
    except Exception:
        return web.Response(status=404)

async def handle_send_emote(request):
    try:
        data = await request.json()
        team_code = data.get("team_code")
        uids = data.get("uids", [])
        emote_id = data.get("emote_id")
        if not team_code or not uids or not emote_id:
            return web.json_response({"success": False, "message": "Missing parameters"})
        try:
            emote_id = int(emote_id)
            uids = [int(uid) for uid in uids]
        except:
            return web.json_response({"success": False, "message": "Invalid UID or Emote ID"})
        success, msg = await cmd_dance(team_code, uids, emote_id)
        return web.json_response({"success": success, "message": msg})
    except Exception as e:
        return web.json_response({"success": False, "message": str(e)})

dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.reply(
        "XcTxTeaM EeMoT Bot\n\nUse /dance [emote_id or name] [team_code] [UID1 UID2 ...]\nExample: /dance 909000045 ABC123 12345678"
    )

@dp.message(Command("dance"))
async def dance_handler(message: Message):
    parts = message.text.split()
    if len(parts) < 4:
        await message.reply("Usage: /dance [emote_id or name] [team_code] [UIDs]")
        return
    emote_input = parts[1]
    emote_id = None
    if emote_input.isdigit():
        emote_id = int(emote_input)
    else:
        emote_id = NAME_TO_ID.get(emote_input.lower())
        if not emote_id:
            await message.reply(f"Emote '{emote_input}' not found")
            return
    team = parts[2]
    uids = [p for p in parts[3:] if p.isdigit()]
    if not uids:
        await message.reply("No valid UIDs provided")
        return
    msg = await message.reply("Sending emote...")
    success, result = await cmd_dance(team, uids, emote_id)
    if success:
        await msg.edit_text(f"✅ {result}")
    else:
        await msg.edit_text(f"❌ Failed: {result}")

async def main():
    if not await login_to_freefire():
        logging.warning("Initial login failed, retrying every 60s")
        while not is_logged_in:
            await asyncio.sleep(60)
            await login_to_freefire()
    asyncio.create_task(periodic_relogin())
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    asyncio.create_task(dp.start_polling(bot))
    app = web.Application()
    app.router.add_get("/", handle_root)
    app.router.add_get("/itemData.json", handle_item_data)
    app.router.add_get("/emote_image/{id}.png", handle_emote_image)
    app.router.add_post("/send_emote", handle_send_emote)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", WEB_PORT)
    await site.start()
    logging.info(f"Website and API running on port {WEB_PORT}")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())