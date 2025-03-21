#!/usr/bin/env python3
import os
import sys
from repello_artemis_sdk import RepelloArtemisClient
from repello_artemis_sdk.enums import ScanType

def main():
    # Get arguments passed from entrypoint.sh
    if len(sys.argv) < 3:
        print("Error: Missing required arguments")
        print("Usage: python main.py <asset_id> <scan_type[,scan_type,...]>")
        sys.exit(1)
        
    asset_id = sys.argv[1]
    scan_types_str = sys.argv[2]
    
    # Get credentials from environment
    client_id = os.environ.get('ARTEMIS_CLIENT_ID')
    client_secret = os.environ.get('ARTEMIS_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("Error: Missing required environment variables ARTEMIS_CLIENT_ID and/or ARTEMIS_CLIENT_SECRET")
        sys.exit(1)
    
    # Map scan type string to enum
    scan_type_map = {
        'quick_scan': ScanType.quick_scan,
        'safety_scan': ScanType.safety_scan,
        'owasp': ScanType.owasp,
        'mitre': ScanType.mitre,
        'nist': ScanType.nist,
        'whistleblower': ScanType.whistleblower,
        'fingerprint': ScanType.fingerprint,
    }
    
    # Split the scan types by comma
    scan_types_list = [st.strip() for st in scan_types_str.split(',')]
    scan_types = []
    
    # Validate each scan type
    for scan_type_str in scan_types_list:
        if scan_type_str not in scan_type_map:
            print(f"Error: Invalid scan type '{scan_type_str}'. Must be one of: {', '.join(scan_type_map.keys())}")
            sys.exit(1)
        scan_types.append(scan_type_map[scan_type_str])
    
    # If only one scan type is provided, use it directly instead of a list
    scan_type_param = scan_types[0] if len(scan_types) == 1 else scan_types
    
    # Initialize client
    client = RepelloArtemisClient(
        client_id,
        client_secret,
        log_to_console=True
    )
    
    # Trigger scan
    print(f"::group::Triggering scan(s) {scan_types_str} for asset {asset_id}")
    try:
        was_scan_triggered = client.assets.trigger_scan(asset_id, scan_type_param)

        if not was_scan_triggered:
            print("::error::Failed to trigger scan")
            print("::endgroup::")
            sys.exit(1)
        
        print("::endgroup::")
        
    except Exception as e:
        print(f"::error::Error during scan: {str(e)}")
        print("::endgroup::")
        sys.exit(1)

if __name__ == "__main__":
    main()
