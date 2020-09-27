#/!bin/bash
mdutil -E /Applications
mdutil -i on /Applications
sleep 60
mdutil -i off /Applications
sudo launchctl unload -w /System/Library/LaunchDaemons/com.apple.metadata.mds.plist
sleep 10
sudo launchctl load -w /System/Library/LaunchDaemons/com.apple.metadata.mds.plist