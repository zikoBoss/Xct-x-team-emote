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
from aiohttp import web
import aiohttp

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties

from xC4 import (
    GenJoinSquadsPacket, Emote_k, ExiT, GeneRaTePk, CrEaTe_ProTo,
    Ua, EnC_PacKeT, DecodE_HeX
)

from Pb2 import MajoRLoGinrEq_pb2, MajoRLoGinrEs_pb2, PorTs_pb2

logging.basicConfig(level=logging.INFO)

# ================== بيانات الحساسة (ضعها هنا للتجربة) ==================
BOT_TOKEN = "8798038134:AAEUlmP2_75Ps7rTe7WkdOElJXpqGt5Cy9c"
FF_UID = "4812753412"
FF_PASSWORD = "492C6754CD1BB892C11548121956ADF254468453FA0A7A25FA6367F9DF926221"
WEB_PORT = int(os.environ.get("PORT", 8080))

# ================== متغيرات الاتصال ==================
online_writer = None
whisper_writer = None
key = None
iv = None
region = None
is_logged_in = False
login_lock = asyncio.Lock()

# ================== تحميل الإيموجيات من itemData.json ==================
ITEM_DATA_URL = "https://raw.githubusercontent.com/4737647734/Emote/main/itemData.json"
ALL_EMOTE = {}  # {id: name} أو العكس؟ سنبني خريطة رقم الرقصة (المستخدم) -> id
# في الموقع سنستخدم id مباشرة، وللبوت سنسمح باستخدام id أو الاسم.

# تحميل البيانات
async def load_emotes():
    global ALL_EMOTE
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(ITEM_DATA_URL) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    # نبني قاموس {id: name} وللبوت سنبني أيضاً من الاسم إلى id
                    name_to_id = {}
                    for item in data:
                        name_to_id[item["name"].lower()] = item["Id"]
                    ALL_EMOTE = name_to_id
                    logging.info(f"Loaded {len(data)} emotes")
                else:
                    logging.error("Failed to load itemData.json")
    except Exception as e:
        logging.error(f"Error loading emotes: {e}")

# ================== دوال تسجيل الدخول (من الكود الأصلي) ==================
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
            if resp.status != 200: return None, None
            data = await resp.json()
            return (data.get("open_id"), data.get("access_token"))

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
                if not data: break
        except:
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
                if not data: break
        except:
            await asyncio.sleep(5)
            whisper_writer = None

async def SEndPacKeT(whisper_writer, online_writer, typE, packet):
    if typE == 'OnLine' and online_writer:
        online_writer.write(packet)
        await online_writer.drain()

async def login_to_freefire():
    global key, iv, region, online_writer, whisper_writer, is_logged_in
    async with login_lock:
        try:
            open_id, access_token = await GeNeRaTeAccEss(FF_UID, FF_PASSWORD)
            if not open_id: return False
            payload = await EncRypTMajoRLoGin(open_id, access_token)
            response = await MajorLogin(payload)
            if not response: return False
            login_res = await DecRypTMajoRLoGin(response)
            url = login_res.url
            region = login_res.region
            token = login_res.token
            bot_uid = login_res.account_uid
            key = login_res.key
            iv = login_res.iv
            timestamp = login_res.timestamp

            login_data = await GetLoginData(url, payload, token)
            if not login_data: return False
            login_dec = await DecRypTLoGinDaTa(login_data)

            online_ip, online_port = login_dec.Online_IP_Port.split(":")
            chat_ip, chat_port = login_dec.AccountIP_Port.split(":")
            auth_token = await xAuThSTarTuP(int(bot_uid), token, int(timestamp), key, iv)

            ready = asyncio.Event()
            asyncio.create_task(run_tcp_chat(chat_ip, int(chat_port), auth_token, ready, region))
            asyncio.create_task(run_tcp_online(online_ip, int(online_port), auth_token))
            await asyncio.wait_for(ready.wait(), timeout=15)
            is_logged_in = True
            logging.info("✅ Logged into Free Fire")
            return True
        except Exception as e:
            logging.error(f"Login failed: {e}")
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

# ================== واجهة الموقع المدمجة (HTML/CSS/JS) ==================
HTML_PAGE = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>XcTxTeaM EeMoT | مكتبة الإيموجيات</title>
<style>
:root {
  --primary: #ffffff;
  --bg-dark: #000000;
  --bg-card: #111111;
  --bg-card-hover: #1c1c1c;
  --text-light: #f5f5f5;
  --text-muted: #999999;
  --border-radius: 16px;
  --transition: all 0.3s ease;
  --glass-bg: rgba(15,15,15,0.85);
  --glass-border: rgba(255,255,255,0.1);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Segoe UI', system-ui, sans-serif;
  background: var(--bg-dark);
  color: var(--text-light);
  direction: rtl;
}
header {
  background: var(--glass-bg);
  backdrop-filter: blur(12px);
  padding: 16px 20px;
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid var(--glass-border);
}
.header-left h1 {
  font-size: 24px;
  background: linear-gradient(135deg, #fff, #888);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.input-panel {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  background: var(--glass-bg);
  backdrop-filter: blur(8px);
  padding: 20px;
  margin: 20px;
  border-radius: var(--border-radius);
  border: 1px solid var(--glass-border);
  justify-content: center;
}
.input-group {
  flex: 1;
  min-width: 150px;
}
.input-group label {
  font-size: 12px;
  color: var(--text-muted);
  display: block;
  margin-bottom: 6px;
}
.input-group input, .uid-input {
  width: 100%;
  background: rgba(0,0,0,0.6);
  border: 1px solid var(--glass-border);
  padding: 10px 12px;
  border-radius: 12px;
  color: white;
  font-size: 14px;
}
.uids-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}
.uid-input { flex: 1; min-width: 100px; }
.add-uid-btn {
  background: linear-gradient(135deg, #fff, #888);
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 12px;
  font-size: 22px;
  cursor: pointer;
  font-weight: bold;
  color: black;
}
.filters { text-align: center; margin: 20px; }
.filters input {
  width: 80%;
  max-width: 500px;
  padding: 12px 20px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: 40px;
  color: white;
  font-size: 16px;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 16px;
  padding: 0 20px 40px;
  max-height: 60vh;
  overflow-y: auto;
}
.card {
  background: var(--bg-card);
  border-radius: 16px;
  padding: 12px;
  text-align: center;
  cursor: pointer;
  transition: var(--transition);
  border: 1px solid var(--glass-border);
}
.card:hover { background: var(--bg-card-hover); transform: translateY(-5px); }
.card img {
  max-width: 80px;
  height: auto;
  border-radius: 12px;
}
.tooltip { font-size: 12px; color: var(--text-muted); margin-top: 8px; word-break: break-all; }
.pagination {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin: 20px;
}
.pagination button {
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  padding: 8px 14px;
  border-radius: 12px;
  color: white;
  cursor: pointer;
}
.pagination button.active { background: linear-gradient(135deg, #fff, #888); color: black; }
footer { text-align: center; padding: 20px; border-top: 1px solid var(--glass-border); color: gray; font-size: 13px; }
footer a { color: #fff; text-decoration: none; }
.toast {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: #222;
  color: white;
  padding: 10px 20px;
  border-radius: 40px;
  z-index: 2000;
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
}
.toast.success { background: #2e7d32; }
.toast.error { background: #c62828; }
.modal {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.9);
  backdrop-filter: blur(12px);
  justify-content: center;
  align-items: center;
  z-index: 3000;
}
.modal-content {
  background: #111;
  padding: 20px;
  border-radius: 24px;
  text-align: center;
  max-width: 300px;
  width: 90%;
}
.modal-content img { max-width: 150px; margin-bottom: 10px; }
.close {
  float: right;
  font-size: 28px;
  cursor: pointer;
}
</style>
</head>
<body>
<header><div class="header-left"><h1>𝕏𝕔𝕋𝕩𝕋𝕖𝕒𝕄 𝔼𝕖𝕄𝕠𝕋</h1></div></header>

<div class="input-panel">
  <div class="input-group">
    <label>🏷️ Team Code</label>
    <input type="text" id="teamCode" placeholder="مثال: ABC123">
  </div>
  <div class="input-group" style="flex:2">
    <label>👥 Player UIDs</label>
    <div style="display:flex; gap:8px; align-items:center;">
      <div id="uidsContainer" style="display:flex; gap:8px; flex-wrap:wrap; flex:1">
        <input type="text" class="uid-input" placeholder="UID">
      </div>
      <button class="add-uid-btn" id="addUidBtn">+</button>
    </div>
  </div>
</div>

<div class="filters"><input type="text" id="searchBox" placeholder="🔍 بحث بالاسم أو المعرف"></div>
<div id="itemsGrid" class="grid">جاري التحميل...</div>
<div class="pagination" id="pagination"></div>
<footer>XcTxTeaM EeMoT | Developed by <a href="https://t.me/ZikoB0SS" target="_blank">@ZikoB0SS</a></footer>

<div id="itemModal" class="modal"><div class="modal-content"><span class="close">&times;</span><img id="modalIcon"><h3 id="modalName"></h3><p id="modalId"></p></div></div>

<script>
const API_URL = "/send_emote";
const ITEM_DATA_URL = "/itemData.json";
let allItems = [], currentPage = 1, itemsPerPage = 30, filteredItems = [];

async function fetchData() {
  try {
    const res = await fetch(ITEM_DATA_URL);
    allItems = await res.json();
    filteredItems = [...allItems];
    renderItems();
    createOBFilter();
  } catch(e) { console.error(e); }
}

function createOBFilter() {
  const versions = new Set();
  allItems.forEach(item => {
    let idStr = item.Id.toString();
    if(idStr.length>=6) versions.add("OB"+idStr.substring(4,6));
  });
  const sorted = [...versions].sort((a,b)=>parseInt(b.slice(2))-parseInt(a.slice(2)));
  const header = document.querySelector('header');
  const filterDiv = document.createElement('div');
  filterDiv.style.display = 'flex';
  filterDiv.style.gap = '8px';
  filterDiv.style.flexWrap = 'wrap';
  filterDiv.style.marginTop = '10px';
  filterDiv.style.justifyContent = 'center';
  const allBtn = document.createElement('button');
  allBtn.innerText = 'الكل';
  allBtn.style.background = '#333';
  allBtn.style.border = 'none';
  allBtn.style.color = 'white';
  allBtn.style.padding = '6px 12px';
  allBtn.style.borderRadius = '20px';
  allBtn.style.cursor = 'pointer';
  allBtn.onclick = () => { filteredItems = [...allItems]; currentPage=1; renderItems(); };
  filterDiv.appendChild(allBtn);
  sorted.forEach(ob => {
    const btn = document.createElement('button');
    btn.innerText = ob;
    btn.style.background = '#333';
    btn.style.border = 'none';
    btn.style.color = 'white';
    btn.style.padding = '6px 12px';
    btn.style.borderRadius = '20px';
    btn.style.cursor = 'pointer';
    btn.onclick = () => {
      const code = ob.slice(2);
      filteredItems = allItems.filter(item => item.Id.toString().startsWith("9090"+code));
      currentPage = 1;
      renderItems();
    };
    filterDiv.appendChild(btn);
  });
  header.appendChild(filterDiv);
}

function renderItems() {
  const searchTerm = document.getElementById('searchBox').value.toLowerCase();
  let data = filteredItems.filter(item => item.name.toLowerCase().includes(searchTerm) || item.Id.toString().includes(searchTerm));
  const grid = document.getElementById('itemsGrid');
  if(data.length===0){ grid.innerHTML='<div>لا توجد نتائج</div>'; updatePagination(0); return; }
  const start = (currentPage-1)*itemsPerPage;
  const pageItems = data.slice(start, start+itemsPerPage);
  grid.innerHTML = '';
  pageItems.forEach(item => {
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `<img src="https://raw.githubusercontent.com/4737647734/Emote/main/emote_image/${item.Id}.png" onerror="this.src='https://via.placeholder.com/80'"><div class="tooltip">${item.Id}</div>`;
    card.onclick = () => sendEmote(item);
    grid.appendChild(card);
  });
  updatePagination(data.length);
}

function updatePagination(total) {
  const totalPages = Math.ceil(total/itemsPerPage);
  const pagDiv = document.getElementById('pagination');
  if(totalPages<=1){ pagDiv.innerHTML=''; return; }
  pagDiv.innerHTML = '';
  for(let i=1;i<=Math.min(totalPages,5);i++){
    const btn = document.createElement('button');
    btn.innerText = i;
    if(i===currentPage) btn.classList.add('active');
    btn.onclick = () => { currentPage=i; renderItems(); };
    pagDiv.appendChild(btn);
  }
}

function showToast(msg, isError=false){
  const toast = document.createElement('div');
  toast.className = `toast ${isError?'error':'success'}`;
  toast.innerText = msg;
  document.body.appendChild(toast);
  setTimeout(()=>toast.style.opacity='1',10);
  setTimeout(()=>{toast.style.opacity='0'; setTimeout(()=>toast.remove(),300);},3000);
}

async function sendEmote(item){
  const teamCode = document.getElementById('teamCode').value.trim();
  const uids = Array.from(document.querySelectorAll('.uid-input')).map(inp=>inp.value.trim()).filter(v=>v && /^\d+$/.test(v));
  if(!teamCode){ showToast('❌ أدخل كود الفريق', true); return; }
  if(uids.length===0){ showToast('❌ أضف UID واحد على الأقل', true); return; }
  showToast(`⏳ جاري إرسال ${item.name}...`);
  try{
    const res = await fetch(API_URL, {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ team_code: teamCode, uids, emote_id: item.Id })
    });
    const data = await res.json();
    if(data.success) showToast(`✅ ${data.message}`);
    else showToast(`❌ فشل: ${data.message}`, true);
  } catch(e){ showToast('❌ خطأ في الاتصال', true); }
}

document.getElementById('addUidBtn').onclick = () => {
  const container = document.getElementById('uidsContainer');
  const newInput = document.createElement('input');
  newInput.type = 'text';
  newInput.className = 'uid-input';
  newInput.placeholder = 'UID';
  container.appendChild(newInput);
};

document.getElementById('searchBox').addEventListener('input', ()=>{
  currentPage=1; renderItems();
});

fetchData();
</script>
</body>
</html>
"""

# ================== دوال خادم الويب ==================
async def handle_root(request):
    return web.Response(text=HTML_PAGE, content_type='text/html')

async def handle_item_data(request):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(ITEM_DATA_URL) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return web.json_response(data)
    except:
        pass
    return web.json_response([])

async def handle_send_emote(request):
    try:
        data = await request.json()
        team_code = data.get("team_code")
        uids = data.get("uids", [])
        emote_id = data.get("emote_id")
        if not team_code or not uids or not emote_id:
            return web.json_response({"success": False, "message": "Missing parameters"})
        success, msg = await cmd_dance(team_code, uids, int(emote_id))
        return web.json_response({"success": success, "message": msg})
    except Exception as e:
        return web.json_response({"success": False, "message": str(e)})

# ================== بوت التلغرام ==================
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.reply("👋 XcTxTeaM EeMoT Bot\nاستخدم /dance [رقم_الإيموجي أو اسمه] [كود_الفريق] [UID1 UID2 ...]")

@dp.message(Command("dance"))
async def dance_handler(message: Message):
    parts = message.text.split()
    if len(parts) < 4:
        await message.reply("مثال: /dance 909000045 ABC123 12345678")
        return
    emote_input = parts[1]
    # محاولة تحويل إلى int أو البحث بالاسم
    if emote_input.isdigit():
        emote_id = int(emote_input)
    else:
        # البحث في ALL_EMOTE (تم تحميله مسبقاً)
        emote_id = ALL_EMOTE.get(emote_input.lower())
        if not emote_id:
            await message.reply(f"❌ الإيموجي '{emote_input}' غير موجود")
            return
    team = parts[2]
    uids = [p for p in parts[3:] if p.isdigit()]
    if not uids:
        await message.reply("❌ لم يتم إدخال UIDs صحيحة")
        return
    msg = await message.reply("💃 جاري الأداء...")
    success, result = await cmd_dance(team, uids, emote_id)
    await msg.edit_text(f"{'✅' if success else '❌'} {result}")

# ================== التشغيل الرئيسي ==================
async def main():
    await load_emotes()
    if not await login_to_freefire():
        logging.warning("فشل تسجيل الدخول الأولي، سيتم إعادة المحاولة كل 60 ثانية")
        while not is_logged_in:
            await asyncio.sleep(60)
            await login_to_freefire()
    asyncio.create_task(periodic_relogin())
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    asyncio.create_task(dp.start_polling(bot))
    app = web.Application()
    app.router.add_get("/", handle_root)
    app.router.add_get("/itemData.json", handle_item_data)
    app.router.add_post("/send_emote", handle_send_emote)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", WEB_PORT)
    await site.start()
    logging.info(f"🚀 Website and API running on port {WEB_PORT}")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())