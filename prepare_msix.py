import os
from PIL import Image, ImageOps

def create_msix_assets():
    icon_path = "icon.png"
    assets_dir = "msix_assets"
    
    if not os.path.exists(icon_path):
        print(f"Error: {icon_path} is missing. Please generate it first.")
        return False
        
    os.makedirs(assets_dir, exist_ok=True)
    img = Image.open(icon_path)
    
    # Store logo sizes
    sizes = {
        "StoreLogo.png": (50, 50),
        "Square150x150Logo.png": (150, 150),
        "Square44x44Logo.png": (44, 44),
        "Wide310x150Logo.png": (310, 150),
        "SplashScreen.png": (620, 300)
    }
    
    for filename, size in sizes.items():
        out_path = os.path.join(assets_dir, filename)
        
        # Special fitting for wide tiles and splash screens
        if filename in ["Wide310x150Logo.png", "SplashScreen.png"]:
            # Create dark background matching our app styling theme (#0f111a)
            bg = Image.new("RGBA", size, (15, 17, 26, 255))
            # Resize the icon to fit vertically inside the tile/splash
            target_h = int(size[1] * 0.7)
            target_w = int(img.width * (target_h / img.height))
            resized_icon = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            # Paste the icon into the center
            offset = ((size[0] - target_w) // 2, (size[1] - target_h) // 2)
            bg.paste(resized_icon, offset, resized_icon if resized_icon.mode == 'RGBA' else None)
            bg.save(out_path, format="PNG")
        else:
            # Resize directly
            resized = img.resize(size, Image.Resampling.LANCZOS)
            resized.save(out_path, format="PNG")
            
        print(f"Generated MSIX asset: {out_path} ({size[0]}x{size[1]})")
        
    return True

def create_manifest():
    manifest_content = """<?xml version="1.0" encoding="utf-8"?>
<Package xmlns="http://schemas.microsoft.com/appx/manifest/foundation/windows10"
         xmlns:uap="http://schemas.microsoft.com/appx/manifest/uap/windows10"
         xmlns:rescap="http://schemas.microsoft.com/appx/manifest/foundation/windows10/restrictedcapabilities"
         IgnorableNamespaces="uap rescap">
  
  <!-- Identity values MUST match the ones assigned in the Microsoft Store Partner Center -->
  <Identity Name="Hyeonseok.DocsTool"
            Publisher="CN=PlaceholderPublisher"
            Version="1.0.0.0"
            ProcessorArchitecture="x64" />

  <Properties>
    <DisplayName>Docs Tool</DisplayName>
    <PublisherDisplayName>Hyeonseok</PublisherDisplayName>
    <Logo>msix_assets\\StoreLogo.png</Logo>
  </Properties>

  <Resources>
    <Resource Language="ko-KR" />
    <Resource Language="en-US" />
  </Resources>

  <Dependencies>
    <TargetDeviceFamily Name="Windows.Desktop"
                        MinVersion="10.0.17763.0"
                        MaxVersionTested="10.0.22621.0" />
  </Dependencies>

  <Capabilities>
    <!-- Essential capability to allow desktop PyInstaller exe to run with full trust -->
    <rescap:Capability Name="runFullTrust" />
  </Capabilities>

  <Applications>
    <Application Id="DocsToolApp"
                 Executable="DocsTool.exe"
                 EntryPoint="Windows.FullTrustApplication">
      <uap:VisualElements DisplayName="Docs Tool"
                          Description="PDF Utility Suite for Conversion, Merging, and Security"
                          BackgroundColor="#0f111a"
                          Square150x150Logo="msix_assets\\Square150x150Logo.png"
                          Square44x44Logo="msix_assets\\Square44x44Logo.png">
        <uap:DefaultTile ShortName="Docs Tool" Wide310x150Logo="msix_assets\\Wide310x150Logo.png">
          <uap:ShowNameOnTiles>
            <uap:ShowOn Tile="square150x150Logo" />
            <uap:ShowOn Tile="wide310x150Logo" />
          </uap:ShowNameOnTiles>
        </uap:DefaultTile>
        <uap:SplashScreen Image="msix_assets\\SplashScreen.png" />
      </uap:VisualElements>
    </Application>
  </Applications>
</Package>
"""
    manifest_path = "AppxManifest.xml"
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(manifest_content)
    print(f"Generated manifest: {manifest_path}")

if __name__ == "__main__":
    if create_msix_assets():
        create_manifest()
        print("\n🎉 MSIX preparation completed! To configure, edit AppxManifest.xml with your Store Publisher parameters.")
