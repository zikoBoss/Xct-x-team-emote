#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import json
import os
import sys
import ssl
import logging
from datetime import datetime
from pathlib import Path

import aiohttp
from aiohttp import web
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
logger = logging.getLogger(__name__)

# ================== إعدادات ==================
BOT_TOKEN = "8798038134:AAEUlmP2_75Ps7rTe7WkdOElJXpqGt5Cy9c"
FF_UID = "4812753412"
FF_PASSWORD = "492C6754CD1BB892C11548121956ADF254468453FA0A7A25FA6367F9DF926221"
WEB_PORT = int(os.environ.get("PORT", 8080))

# ================== تحميل الإيموجيات من itemData.json مباشرة ==================
item_data_path = Path("itemData.json")
if not item_data_path.exists():
    logger.error("itemData.json not found!")
    sys.exit(1)

with open(item_data_path, "r", encoding="utf-8") as f:
    item_data_list = json.load(f)

# بناء خريطة: الرقم التسلسلي (1,2,3...) -> المعرف الكبير
# وبنفس الوقت نبني قائمة للموقع (نفس itemData_list)
emote_number_to_id = {}
emote_id_to_number = {}
for idx, item in enumerate(item_data_list, start=1):
    idd = item["Id"]
    emote_number_to_id[idx] = idd
    emote_id_to_number[idd] = idx

logger.info(f"Loaded {len(emote_number_to_id)} emotes from itemData.json")

# ================== متغيرات الاتصال (نفس البوت الأصلي) ==================
online_writer = None
whisper_writer = None
key = None
iv = None
region = None

# ================== دوال تسجيل الدخول (من البوت الأصلي) ==================
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
    global key, iv, region, online_writer, whisper_writer
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
        return True
    except Exception as e:
        logger.error(f"Login failed: {e}")
        return False

async def cmd_dance(team_code, uids, emote_number):
    emote_id = emote_number_to_id.get(emote_number)
    if not emote_id:
        return False, f"❌ رقم الرقصة {emote_number} غير موجود"
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
        return True, f"✅ تم أداء الرقصة {emote_number} للأهداف: {', '.join(uids)}"
    except Exception as e:
        logger.error(f"Dance error: {e}")
        return False, f"❌ فشل: {str(e)}"

# ================== خادم الويب والموقع (مدمج) ==================
HTML_PAGE = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>XcTxTeaM EeMoT | مكتبة الإيموجيات</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', system-ui, sans-serif; background: #000; color: #fff; direction: rtl; }
        header { background: rgba(10,10,10,0.9); backdrop-filter: blur(10px); padding: 15px 20px; position: sticky; top: 0; border-bottom: 1px solid #222; }
        h1 { font-size: 1.8rem; background: linear-gradient(135deg, #fff, #aaa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .input-panel { display: flex; flex-wrap: wrap; gap: 15px; background: #111; margin: 20px; padding: 20px; border-radius: 20px; }
        .input-group { flex: 1; min-width: 150px; }
        .input-group label { font-size: 12px; color: #aaa; display: block; margin-bottom: 6px; }
        .input-group input, .uid-input { width: 100%; background: #1a1a1a; border: 1px solid #333; padding: 10px 12px; border-radius: 12px; color: white; }
        .uids-wrapper { display: flex; gap: 8px; align-items: center; }
        #uidsContainer { display: flex; flex-wrap: wrap; gap: 8px; flex: 1; }
        .uid-input { flex: 1; min-width: 100px; }
        .add-uid-btn { background: #fff; border: none; width: 40px; height: 40px; border-radius: 12px; font-size: 24px; cursor: pointer; font-weight: bold; }
        .filters { text-align: center; margin: 20px; }
        .filters input { width: 80%; max-width: 500px; background: #1a1a1a; border: 1px solid #333; padding: 12px 20px; border-radius: 40px; color: white; }
        .ob-filters { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin: 10px 20px; }
        .ob-btn { background: #222; border: none; padding: 6px 14px; border-radius: 30px; color: #ccc; cursor: pointer; }
        .ob-btn.active { background: #fff; color: #000; font-weight: bold; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 16px; padding: 0 20px 40px; max-height: 55vh; overflow-y: auto; }
        .card { background: #111; border-radius: 20px; padding: 12px; text-align: center; cursor: pointer; transition: 0.2s; border: 1px solid #222; }
        .card:hover { background: #1a1a1a; transform: translateY(-3px); }
        .card img { width: 80px; height: 80px; object-fit: contain; border-radius: 12px; }
        .tooltip { font-size: 12px; color: #888; margin-top: 8px; word-break: break-all; }
        .pagination { display: flex; justify-content: center; gap: 8px; margin: 20px; }
        .pagination button { background: #222; border: none; padding: 8px 14px; border-radius: 12px; color: white; cursor: pointer; }
        .pagination button.active { background: #fff; color: black; }
        footer { text-align: center; padding: 20px; border-top: 1px solid #222; color: #666; }
        footer a { color: #fff; text-decoration: none; }
        .toast { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); background: #222; color: white; padding: 10px 20px; border-radius: 40px; z-index: 2000; opacity: 0; transition: opacity 0.3s; pointer-events: none; }
        .toast.success { background: #2e7d32; }
        .toast.error { background: #c62828; }
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); backdrop-filter: blur(12px); justify-content: center; align-items: center; z-index: 3000; }
        .modal-content { background: #111; padding: 24px; border-radius: 32px; text-align: center; max-width: 280px; }
        .modal-content img { width: 120px; }
        .close { float: right; font-size: 28px; cursor: pointer; }
        @media (max-width: 600px) { .grid { grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); } }
    </style>
</head>
<body>
<header><h1>𝕏𝕔𝕋𝕩𝕋𝕖𝕒𝕄 𝔼𝕖𝕄𝕠𝕋</h1></header>
<div class="input-panel">
    <div class="input-group"><label>🏷️ كود الفريق</label><input type="text" id="teamCode" placeholder="مثال: ABC123"></div>
    <div class="input-group" style="flex:2">
        <label>👥 معرفات اللاعبين (UID)</label>
        <div class="uids-wrapper">
            <div id="uidsContainer"><input type="text" class="uid-input" placeholder="UID"></div>
            <button class="add-uid-btn" id="addUidBtn">+</button>
        </div>
    </div>
</div>
<div class="filters"><input type="text" id="searchBox" placeholder="🔍 بحث بالاسم أو المعرف"></div>
<div id="obFilterContainer" class="ob-filters"></div>
<div id="itemsGrid" class="grid">جاري التحميل...</div>
<div class="pagination" id="pagination"></div>
<footer>XcTxTeaM EeMoT | <a href="https://t.me/ZikoB0SS" target="_blank">@ZikoB0SS</a></footer>
<div id="itemModal" class="modal"><div class="modal-content"><span class="close">&times;</span><img id="modalIcon"><h3 id="modalName"></h3><p id="modalId"></p></div></div>
<script>
    const API_URL = "/send_emote";
    const ITEM_DATA_URL = "/itemData.json";
    let allItems = [], currentPage = 1, itemsPerPage = 30, filteredItems = [];
    async function fetchData() {
        try {
            const res = await fetch(ITEM_DATA_URL);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            allItems = await res.json();
            filteredItems = [...allItems];
            renderItems();
            buildOBFilters();
        } catch(e) { console.error(e); document.getElementById('itemsGrid').innerHTML = '<div style="text-align:center">فشل التحميل</div>'; }
    }
    function buildOBFilters() {
        const versions = new Set();
        allItems.forEach(item => { let idStr = item.Id.toString(); if(idStr.length>=6) versions.add("OB"+idStr.substring(4,6)); });
        const sorted = [...versions].sort((a,b)=>parseInt(b.slice(2))-parseInt(a.slice(2)));
        const container = document.getElementById('obFilterContainer');
        container.innerHTML = '<button class="ob-btn" data-ob="all">الكل</button>';
        sorted.forEach(ob => { const btn = document.createElement('button'); btn.className='ob-btn'; btn.innerText=ob; btn.dataset.ob=ob; btn.onclick=()=>filterByOB(ob); container.appendChild(btn); });
    }
    function filterByOB(ob) { activeOB = (ob==='all')?null:ob; if(activeOB) { const code=activeOB.slice(2); filteredItems=allItems.filter(item=>item.Id.toString().startsWith("9090"+code)); } else { filteredItems=[...allItems]; } currentPage=1; renderItems(); }
    function renderItems() {
        const searchTerm = document.getElementById('searchBox').value.toLowerCase();
        let data = filteredItems.filter(item => item.name.toLowerCase().includes(searchTerm) || item.Id.toString().includes(searchTerm));
        const grid = document.getElementById('itemsGrid');
        if(data.length===0){ grid.innerHTML='<div style="text-align:center">لا توجد نتائج</div>'; return; }
        const start = (currentPage-1)*itemsPerPage;
        const pageItems = data.slice(start, start+itemsPerPage);
        grid.innerHTML = '';
        pageItems.forEach((item, idx) => {
            const card = document.createElement('div'); card.className='card';
            const imgSrc = `/emote_image/${item.Id}.png`;
            card.innerHTML = `<img src="${imgSrc}" onerror="this.src='https://via.placeholder.com/80?text=?'"><div class="tooltip">${item.Id}<br>${item.name}</div>`;
            card.onclick = () => sendEmote(item, idx);
            grid.appendChild(card);
        });
        updatePagination(data.length);
    }
    function updatePagination(total) { const totalPages = Math.ceil(total/itemsPerPage); const pagDiv = document.getElementById('pagination'); if(totalPages<=1){ pagDiv.innerHTML=''; return; } pagDiv.innerHTML=''; for(let i=1;i<=Math.min(totalPages,5);i++){ const btn=document.createElement('button'); btn.innerText=i; if(i===currentPage) btn.classList.add('active'); btn.onclick=()=>{ currentPage=i; renderItems(); }; pagDiv.appendChild(btn); } }
    function showToast(msg, isError=false){ const toast=document.createElement('div'); toast.className=`toast ${isError?'error':'success'}`; toast.innerText=msg; document.body.appendChild(toast); setTimeout(()=>toast.style.opacity='1',10); setTimeout(()=>{ toast.style.opacity='0'; setTimeout(()=>toast.remove(),300); },3000); }
    async function sendEmote(item, index) {
        const teamCode = document.getElementById('teamCode').value.trim();
        const uids = Array.from(document.querySelectorAll('.uid-input')).map(inp=>inp.value.trim()).filter(v=>v && /^\d+$/.test(v));
        if(!teamCode){ showToast('❌ أدخل كود الفريق', true); return; }
        if(uids.length===0){ showToast('❌ أضف UID واحد على الأقل', true); return; }
        const emoteNumber = index + (currentPage-1)*itemsPerPage + 1;
        showToast(`⏳ جاري إرسال ${item.name}...`);
        try{
            const res = await fetch(API_URL, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ team_code: teamCode, uids, emote_number: emoteNumber }) });
            const data = await res.json();
            if(data.success) showToast(`✅ ${data.message}`);
            else showToast(`❌ فشل: ${data.message}`, true);
        } catch(e){ showToast('❌ خطأ في الاتصال بالبوت', true); }
    }
    document.getElementById('addUidBtn').onclick = () => { const container = document.getElementById('uidsContainer'); const newInput = document.createElement('input'); newInput.type='text'; newInput.className='uid-input'; newInput.placeholder='UID'; container.appendChild(newInput); };
    document.getElementById('searchBox').addEventListener('input', ()=>{ currentPage=1; renderItems(); });
    fetchData();
</script>
</body>
</html>
"""

async def handle_root(request):
    return web.Response(text=HTML_PAGE, content_type='text/html')

async def handle_item_data(request):
    return web.json_response(item_data_list)

async def handle_emote_image(request):
    image_name = request.match_info.get('id', '')
    if not image_name:
        return web.Response(status=404)
    image_path = Path("emote_image") / f"{image_name}.png"
    if not image_path.exists():
        return web.Response(status=404)
    try:
        with open(image_path, 'rb') as f:
            return web.Response(body=f.read(), content_type='image/png')
    except Exception:
        return web.Response(status=500)

async def handle_send_emote(request):
    try:
        data = await request.json()
        team_code = data.get("team_code")
        uids = data.get("uids", [])
        emote_number = data.get("emote_number")
        if not team_code or not uids or not emote_number:
            return web.json_response({"success": False, "message": "بيانات ناقصة"})
        success, msg = await cmd_dance(team_code, uids, int(emote_number))
        return web.json_response({"success": success, "message": msg})
    except Exception as e:
        logger.error(f"Error in send_emote: {e}")
        return web.json_response({"success": False, "message": str(e)})

# ================== بوت التلغرام ==================
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.reply(
        "👋 **بوت الرقص المنفصل**\n\n"
        "الاستخدام:\n"
        "`/dance [رقم_الرقصة] [كود_الفريق] [UID1] [UID2] ...`\n\n"
        "مثال:\n"
        "`/dance 5 ABC123 12345678 87654321`",
        parse_mode="Markdown"
    )

@dp.message(Command("dance"))
async def dance_handler(message: Message):
    parts = message.text.split()
    if len(parts) < 4:
        await message.reply("❌ استخدم: `/dance [رقم_الرقصة] [كود_الفريق] [UID1] [UID2] ...`")
        return
    try:
        emote = int(parts[1])
    except:
        await message.reply("❌ رقم الرقصة غير صحيح")
        return
    team = parts[2]
    uids = [p for p in parts[3:] if p.isdigit()]
    if not uids:
        await message.reply("❌ لم يتم تحديد أي UID صحيح")
        return
    msg = await message.reply("💃 جاري أداء الرقصة...")
    success, result = await cmd_dance(team, uids, emote)
    await msg.edit_text(result)

# ================== التشغيل الرئيسي ==================
async def main():
    logger.info("🚀 جاري تسجيل الدخول إلى Free Fire...")
    if not await login_to_freefire():
        logger.error("❌ فشل الاتصال، سيتم إعادة المحاولة كل 30 ثانية")
        while True:
            await asyncio.sleep(30)
            if await login_to_freefire():
                break
    logger.info("✅ متصل. البوت يعمل...")

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
    logger.info(f"🌐 الموقع متاح على المنفذ {WEB_PORT}")

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())