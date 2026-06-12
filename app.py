import streamlit as st
from PIL import Image
import io
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
import webbrowser
import geocoder
import requests
from dotenv import load_dotenv
import os
from datetime import date

# Load .env secrets
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")

# --------------------------------------------
# 🐧 Linux Commands
linux_commands = {
    "Show date": "date",
    "Show calendar": "cal",
    "List files": "ls -al",
    "Show current directory": "pwd",
    "Disk usage": "df -h",
    "Memory usage": "free -m",
    "CPU Info": "lscpu",
    "OS Info": "uname -a",
    "Top 10 processes": "top -b -n1 | head -20",
    "Current user": "whoami",
    "Show logged in users": "who",
    "System uptime": "uptime",
    "IP addresses": "ip a",
    "Network routes": "ip r",
    "Ping google": "ping -c 4 google.com",
    "List environment variables": "printenv",
    "Find file named 'test.txt'": "find / -name test.txt",
    "Search 'root' in /etc/passwd": "grep 'root' /etc/passwd",
    "Create file.txt": "touch file.txt",
    "Create directory 'testdir'": "mkdir testdir",
    "Remove file.txt": "rm file.txt",
    "Remove directory 'testdir'": "rmdir testdir",
    "Copy file.txt to copy.txt": "cp file.txt copy.txt",
    "Rename file.txt to renamed.txt": "mv file.txt renamed.txt",
    "Show file content (/etc/os-release)": "cat /etc/os-release",
    "Append 'Hello' to file.txt": "echo 'Hello' >> file.txt",
    "Change file permissions": "chmod 755 file.txt",
    "Change file owner to root": "chown root:root file.txt",
    "Show running services": "systemctl list-units --type=service",
    "Install 'tree' (apt)": "sudo apt install tree",
    "Update packages": "sudo apt update",
    "Upgrade system": "sudo apt upgrade -y",
    "Remove 'tree' (apt)": "sudo apt remove tree",
    "Check UFW firewall status": "sudo ufw status",
    "Enable UFW firewall": "sudo ufw enable",
    "Disable UFW firewall": "sudo ufw disable",
    "Show hostname": "hostname",
    "Check if port 22 is open": "ss -tuln | grep :22",
    "Reboot system": "sudo reboot",
    "Shutdown system": "sudo shutdown now",
    "List all users": "cut -d: -f1 /etc/passwd",
    "List cron jobs": "crontab -l",
    "Check open ports (netstat)": "netstat -tuln",
    "Download file with wget": "wget http://example.com",
    "Check SELinux status": "sestatus",
    "Show kernel logs": "dmesg | tail -20",
    "Show mounted filesystems": "mount | column -t",
    "Display system journal": "journalctl -xe",
    "Show current processes": "ps aux",
    "Kill process by PID": "kill -9 <PID>",
    "Check disk space of /": "du -sh /",
    "View network interfaces": "ifconfig",
    "Traceroute to google": "traceroute google.com",
    "List installed packages (Debian)": "dpkg -l",
    "Check system load": "uptime"
}

# 🐳 Docker Commands
docker_commands = {
#  "Launch new Ubuntu container": "docker run -dit --name mycontainer ubuntu",
    "Start container": "docker start mycontainer",
    "Stop container": "docker stop mycontainer",
    "Restart container": "docker restart mycontainer",
    "Remove container": "docker rm mycontainer",
    "List containers": "docker ps -a",
    "List running containers": "docker ps",
    "List Docker images": "docker images",
    "Pull Ubuntu image": "docker pull ubuntu",
    "Remove image": "docker rmi ubuntu",
    "Show Docker version": "docker version",
    "Show Docker info": "docker info",
    "Show container logs": "docker logs mycontainer",
    "Build Docker image": "docker build -t myimage .",
    "Save Docker image to file": "docker save -o image.tar myimage",
    "Load Docker image from file": "docker load -i image.tar",
    "Tag Docker image": "docker tag myimage newname",
    "Push image to DockerHub": "docker push myimage",
    "Prune unused images": "docker image prune -f",
    "Run Apache Webserver (port 8080)": "docker run -dit --name webserver -p 8080:80 httpd",
    "Run Nginx server (port 8081)": "docker run -dit --name nginx -p 8081:80 nginx",
    "View Docker network": "docker network ls",
    "Inspect container": "docker inspect mycontainer",
    "Check container stats": "docker stats",
    "Run interactive bash in container": "docker exec -it mycontainer bash",
    "View container file system": "docker exec -it mycontainer ls /",
    "Create Docker volume": "docker volume create myvol",
    "List Docker volumes": "docker volume ls",
    "Run with mounted volume": "docker run -dit -v myvol:/data ubuntu",
    "Create Docker network": "docker network create mynet",
    "Run container with custom network": "docker run -dit --network=mynet --name custom ubuntu",
    "List Docker contexts": "docker context ls",
    "Switch Docker context": "docker context use default",
    "Export container": "docker export mycontainer > mycontainer.tar",
    "Import container": "docker import mycontainer.tar",
    "List Docker events": "docker events",
    "Docker login": "docker login",
    "Docker logout": "docker logout",
    "Show Docker help": "docker --help",
    "Docker compose version": "docker-compose version",
    "List Docker compose services": "docker-compose ps",
    "Start Docker compose services": "docker-compose up -d",
    "Stop Docker compose services": "docker-compose down"
}

# Dummy SSH runner
def run_remote_command(user, ip, command):
    # Replace with real SSH execution logic
    return f"Executed '{command}' on {ip} as {user}"

# --------------------------------------------
# 📋 Sidebar Menu
st.sidebar.title("📋 Task Menu")
menu = st.sidebar.radio(
    "Select a Task",
    [
        "📸 Capture Photo",
        "📧 Send Email",
        "📱 Send WhatsApp Message",
        "📲 Send SMS",
        "📍 Show My Location",
        "🗺️ Show Route",
        "🛒 Find Nearby Grocery Stores",
        "🌐 Get IP Address & Location",
        "🎥 Record & Send Video",
        "📞 Make Voice Call",
        "🐧 Run Linux Commands",
        "🐳 Run Docker Commands",
        "🤖 Gemini Assistant",
    ]
)

# --------------------------------------------
# 🐧 Linux Commands
if menu == "🐧 Run Linux Commands":
    st.title("🐧 Run Linux Command")

    selected = st.selectbox("Select Command", list(linux_commands.keys()))
    if st.button("Select Command"):
        st.success(f"Selected: {selected}")
        st.code(linux_commands[selected], language="bash")

    user = st.text_input("SSH Username")
    ip = st.text_input("Remote IP")
    if st.button("Run Command"):
        result = run_remote_command(user, ip, linux_commands[selected])
        st.code(result, language="bash")

# --------------------------------------------
# 🐳 Docker Commands
elif menu == "🐳 Run Docker Commands":
    st.title("🐳 Run Docker Command")

    selected = st.selectbox("Select Command", list(docker_commands.keys()))
    if st.button("Select Command"):
        st.success(f"Selected: {selected}")
        st.code(docker_commands[selected], language="bash")

    user = st.text_input("SSH Username")
    ip = st.text_input("Remote IP")
    if st.button("Run Command"):
        result = run_remote_command(user, ip, docker_commands[selected])
        st.code(result, language="bash")

# --------------------------------------------
# 📸 Capture Photo
elif menu == "📸 Capture Photo":
    st.title("📸 Capture Photo")
    captured_image = st.camera_input("Take a photo")
    if captured_image:
        img = Image.open(captured_image)
        st.image(img, caption="Captured Photo", use_column_width=True)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        href = f'<a href="data:file/png;base64,{b64}" download="captured_photo.png">📥 Download Photo</a>'
        st.markdown(href, unsafe_allow_html=True)

# 📧 Send Email
elif menu == "📧 Send Email":
    st.title("📧 Send Email")
    recipient = st.text_input("Recipient Email")
    subject = st.text_input("Subject")
    body = st.text_area("Message Body")
    if st.button("Send Email"):
        if recipient:
            try:
                msg = MIMEMultipart()
                msg['From'] = EMAIL_USER
                msg['To'] = recipient
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(EMAIL_USER, EMAIL_PASS)
                server.sendmail(EMAIL_USER, recipient, msg.as_string())
                server.quit()
                st.success(f"✅ Email sent to {recipient}")
            except Exception as e:
                st.error(f"❌ Error: {e}")
        else:
            st.warning("Please enter recipient email.")

# 📱 WhatsApp Message
elif menu == "📱 Send WhatsApp Message":
    st.title("📱 Send WhatsApp Message")
    whatsapp_msg = st.text_area("WhatsApp Message")
    if st.button("Open WhatsApp"):
        if whatsapp_msg:
            encoded_msg = whatsapp_msg.replace(" ", "%20").replace("\n", "%0A")
            url = f"https://wa.me/?text={encoded_msg}"
            webbrowser.open_new_tab(url)
        else:
            st.warning("Please enter a message!")

# 📲 Send SMS
elif menu == "📲 Send SMS":
    st.title("📲 Send SMS")
    sms_to = st.text_input("Recipient Phone Number (+91...)")
    sms_msg = st.text_area("SMS Message")
    if st.button("Send SMS"):
        if sms_to and sms_msg:
            try:
                client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
                client.messages.create(body=sms_msg, from_=TWILIO_PHONE, to=sms_to)
                st.success(f"✅ SMS sent to {sms_to}")
            except Exception as e:
                st.error(f"❌ Error: {e}")
        else:
            st.warning("Please enter phone and message!")

# 📍 Show My Location
elif menu == "📍 Show My Location":


    st.title("📍 My Current Location")
    if st.button("Get My Location"):
        g = geocoder.ip('me')
        if g.ok:
            st.write(f"📍 Latitude: {g.latlng[0]}, Longitude: {g.latlng[1]}")
            maps_url = f"https://www.google.com/maps?q={g.latlng[0]},{g.latlng[1]}"
            st.markdown(f"[🌍 Open in Google Maps]({maps_url})")
        else:
            st.warning("Could not detect location.")

# 🗺️ Show Route
elif menu == "🗺️ Show Route":
    st.title("🗺️ Show Route")
    destination = st.text_input("Destination Address")
    if st.button("Show Route"):
        g = geocoder.ip('me')
        if g.ok and destination:
            origin = f"{g.latlng[0]},{g.latlng[1]}"
            route_url = f"https://www.google.com/maps/dir/{origin}/{destination}"
            webbrowser.open_new_tab(route_url)
        else:
            st.warning("Could not detect location or missing destination.")

# 🛒 Find Nearby Grocery Stores
elif menu == "🛒 Find Nearby Grocery Stores":
    st.title("🛒 Find Nearby Grocery Stores")
    if st.button("Find Grocery Stores"):
        g = geocoder.ip('me')
        if g.ok:
            maps_url = f"https://www.google.com/maps/search/grocery+stores/@{g.latlng[0]},{g.latlng[1]},15z"
            webbrowser.open_new_tab(maps_url)
        else:
            st.warning("Could not detect location.")

# 🌐 Get IP Address & Location
elif menu == "🌐 Get IP Address & Location":
    st.title("🌐 Get IP & Location")
    if st.button("Get IP Info"):
        try:
            ip = requests.get('https://api.ipify.org').text
            g = geocoder.ip('me')
            st.write(f"💻 IP Address: {ip}")
            if g.ok:
                st.write(f"📍 Location: {g.city}, {g.state}, {g.country}")
            else:
                st.warning("Could not get detailed location.")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# 🎥 Record & Send Video - your JS/HTML stays same (use st.components.v1.html)

# 📞 Make Voice Call
elif menu == "📞 Make Voice Call":
    st.title("📞 Make Voice Call")
    to_number = st.text_input("Recipient Phone Number (+91...)")
    message_text = st.text_area("Message to Speak")
    if st.button("Call Now"):
        if to_number and message_text:
            try:
                from urllib.parse import quote
                twiml_message = quote(message_text)
                twiml_url = f"http://twimlets.com/message?Message%5B0%5D={twiml_message}"
                client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
                call = client.calls.create(
                    to=to_number,
                    from_=TWILIO_PHONE,
                    url=twiml_url
                )
                st.success(f"✅ Call initiated to {to_number} (SID: {call.sid})")
            except Exception as e:
                st.error(f"❌ Error: {e}")
        else:
            st.warning("Please enter phone and message.")

# 🤖 Gemini Assistant
# 🧠 Gemini Assistant Section
import google.generativeai as genai

# Load Gemini API key from your .env file or directly here
import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

if menu == "🤖 Gemini Assistant":
    st.title("🤖 Gemini AI Assistant")

    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    user_input = st.text_area("Ask me anything!", "", height=100)

    if st.button("Ask Gemini"):
        if user_input.strip() == "":
            st.warning("Please enter a question.")
        else:
            # Initialize Gemini model
            model = genai.GenerativeModel('gemini-pro')
            chat = model.start_chat(history=st.session_state['chat_history'])

            response = chat.send_message(user_input)

            st.session_state['chat_history'].append({
                "role": "user",
                "parts": [user_input]
            })
            st.session_state['chat_history'].append({
                "role": "model",
                "parts": [response.text]
            })

    # Display chat history
    for msg in st.session_state['chat_history']:
        if msg["role"] == "user":
            st.write(f"🧑‍💻 **You:** {msg['parts'][0]}")
        else:
            st.write(f"🤖 **Gemini:** {msg['parts'][0]}")

            
