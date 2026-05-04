"""
Startup Test Script
Tests that the server can start without crashing
"""

import subprocess
import time
import sys
import requests

def test_startup():
    """Test server startup"""
    print("=" * 70)
    print("Testing NexusAI Server Startup")
    print("=" * 70)
    
    print("\n1. Starting server...")
    
    # Start server in subprocess
    try:
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("   Server process started (PID: {})".format(process.pid))
        print("   Waiting 60 seconds for startup...")
        
        # Wait up to 60 seconds for startup
        for i in range(60):
            time.sleep(1)
            
            # Check if process crashed
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                print("\n❌ Server crashed during startup!")
                print("\nSTDOUT:")
                print(stdout)
                print("\nSTDERR:")
                print(stderr)
                return False
            
            # Try to connect
            try:
                response = requests.get("http://localhost:8000/api/health", timeout=1)
                if response.status_code == 200:
                    print("\n✓ Server started successfully!")
                    print(f"   Startup time: {i+1} seconds")
                    
                    # Get health info
                    health = response.json()
                    print(f"\n   Status: {health.get('status')}")
                    print(f"   Loaded adapters: {health.get('loaded_adapters')}")
                    print(f"   Sentiment model: {health.get('sentiment_model_loaded')}")
                    print(f"   Vector builder: {health.get('vector_builder_active')}")
                    
                    # Shutdown server
                    print("\n2. Shutting down server...")
                    process.terminate()
                    process.wait(timeout=10)
                    print("   ✓ Server shut down cleanly")
                    
                    return True
            except requests.RequestException:
                pass  # Server not ready yet
            
            if (i + 1) % 10 == 0:
                print(f"   Still waiting... ({i+1}s)")
        
        # Timeout
        print("\n❌ Server startup timeout (>60 seconds)")
        process.terminate()
        stdout, stderr = process.communicate(timeout=5)
        print("\nLast output:")
        print(stdout[-500:] if len(stdout) > 500 else stdout)
        return False
        
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        try:
            process.terminate()
        except:
            pass
        return False

if __name__ == "__main__":
    print("\nIMPORTANT: This will start the server and test it.")
    print("Make sure no other instance is running on port 8000.\n")
    
    input("Press Enter to start test...")
    
    success = test_startup()
    
    print("\n" + "=" * 70)
    if success:
        print("✅ STARTUP TEST PASSED")
        print("\nThe server can start without crashing!")
    else:
        print("❌ STARTUP TEST FAILED")
        print("\nCheck the error output above for details.")
    print("=" * 70)
    
    sys.exit(0 if success else 1)
