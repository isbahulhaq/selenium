import subprocess

# Install wget
subprocess.run(['apt', 'install', 'wget', '-y'])

# Install webdriver_manager
subprocess.run(['pip', 'install', 'webdriver_manager'])

# Upgrade webdriver_manager
subprocess.run(['pip', 'install', '--upgrade', 'webdriver_manager'])

# Install curl
subprocess.run(['apt', 'install', 'curl'])

# Download Brave browser archive keyring
subprocess.run(['curl', '-fsSLo', '/usr/share/keyrings/brave-browser-archive-keyring.gpg', 'https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg'])

# Add Brave browser repository to sources.list.d
subprocess.run(['echo', 'deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main', '|', 'sudo', 'tee', '/etc/apt/sources.list.d/brave-browser-release.list'])

# Update apt
subprocess.run(['apt', 'update'])

# Install Brave browser
subprocess.run(['apt', 'install', 'brave-browser'])

# Install playwright
subprocess.run(['pip', 'install', 'playwright'])

# Install Playwright dependencies
subprocess.run(['playwright', 'install'])

# Install indian_names
subprocess.run(['pip', 'install', 'indian_names'])
