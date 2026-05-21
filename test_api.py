import json
import urllib.request
import urllib.error
import time

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print("[INFO] Starting URL Shortener API Tests...")
    
    # 1. Test Health Check
    try:
        response = urllib.request.urlopen(f"{BASE_URL}/health")
        data = json.loads(response.read().decode())
        print(f"[SUCCESS] Health Check Passed: {data}")
    except Exception as e:
        print(f"[ERROR] Health Check Failed: {e}\nIs the server running on {BASE_URL}?")
        return

    # 2. Test Shortening a Valid URL
    target_url = "https://github.com/fastapi/fastapi"
    payload = {"original_url": target_url}
    req = urllib.request.Request(
        f"{BASE_URL}/shorten",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    short_code = None
    short_url = None
    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode())
        print(f"[SUCCESS] Shorten URL Passed: {data}")
        short_code = data.get("short_code")
        short_url = data.get("short_url")
    except Exception as e:
        print(f"[ERROR] Shorten URL Failed: {e}")
        return

    # 3. Test Validation: Invalid URL
    invalid_payload = {"original_url": "not-a-valid-url"}
    req_invalid = urllib.request.Request(
        f"{BASE_URL}/shorten",
        data=json.dumps(invalid_payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        urllib.request.urlopen(req_invalid)
        print("[ERROR] Validation Failed: Allowed an invalid URL!")
    except urllib.error.HTTPError as e:
        if e.code == 422:
            print("[SUCCESS] Validation Passed: Correctly rejected invalid URL (HTTP 422)")
        else:
            print(f"[ERROR] Validation Failed with unexpected code: {e.code}")

    # 4. Test Redirection (HTTP 307)
    if short_code:
        # We need a custom opener to inspect the HTTP 307 redirect instead of auto-following it
        class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                # Raise an error to stop redirection and let us catch it
                raise urllib.error.HTTPError(req.full_url, code, msg, headers, fp)

        opener = urllib.request.build_opener(NoRedirectHandler)
        try:
            # We fetch /short_code directly using our special opener
            opener.open(f"{BASE_URL}/{short_code}")
            print(f"[ERROR] Redirection Test Failed: Did not redirect.")
        except urllib.error.HTTPError as e:
            if e.code == 307:
                redirect_target = e.headers.get("Location")
                if redirect_target == target_url:
                    print(f"[SUCCESS] Redirection Passed: Redirected to {redirect_target} (HTTP 307)")
                else:
                    print(f"[ERROR] Redirection Target Mismatch: Expected {target_url}, got {redirect_target}")
            else:
                print(f"[ERROR] Redirection Test Failed: HTTP {e.code}")
        except Exception as e:
            print(f"[ERROR] Redirection unexpected error: {e}")

    # 5. Test 404 for Missing Code
    try:
        urllib.request.urlopen(f"{BASE_URL}/nonexistent123")
        print("[ERROR] Missing Code Test Failed: Returned HTTP 200 for missing code!")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("[SUCCESS] Missing Code Passed: Returned HTTP 404")
        else:
            print(f"[ERROR] Missing Code Failed with unexpected code: {e.code}")

    print("\n[INFO] API verification complete!")

if __name__ == "__main__":
    run_tests()
