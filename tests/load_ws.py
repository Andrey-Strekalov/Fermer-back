#!/usr/bin/env python
"""
WebSocket load tester for the notifications endpoint.

Usage:
    python tests/load_ws.py --token <access_token> --count 100 --duration 10
"""
import argparse
import asyncio
import statistics
import time

import websockets
from websockets.exceptions import ConnectionClosedError, WebSocketException


async def _connect_and_hold(uri: str, duration: float, stats: dict) -> None:
    t0 = time.monotonic()
    try:
        async with websockets.connect(uri, open_timeout=10) as ws:
            stats['connect_ms'].append((time.monotonic() - t0) * 1000)
            stats['success'] += 1

            deadline = time.monotonic() + duration
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    break
                try:
                    await asyncio.wait_for(ws.recv(), timeout=min(remaining, 1.0))
                    stats['messages'] += 1
                except asyncio.TimeoutError:
                    pass

    except ConnectionRefusedError:
        stats['err_refused'] += 1
    except asyncio.TimeoutError:
        stats['err_timeout'] += 1
    except ConnectionClosedError as exc:
        if exc.code == 4001:
            stats['err_4001'] += 1
        else:
            stats['err_other'] += 1
    except WebSocketException:
        stats['err_other'] += 1
    except OSError:
        stats['err_refused'] += 1
    except Exception:
        stats['err_other'] += 1


async def _run(url: str, token: str, count: int, duration: float) -> dict:
    stats: dict = {
        'success': 0,
        'messages': 0,
        'connect_ms': [],
        'err_4001': 0,
        'err_refused': 0,
        'err_timeout': 0,
        'err_other': 0,
    }
    uri = f"{url.rstrip('/')}/?token={token}"
    await asyncio.gather(*[_connect_and_hold(uri, duration, stats) for _ in range(count)])
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description='WebSocket load tester')
    parser.add_argument('--url', default='ws://127.0.0.1:8000/ws/notifications/')
    parser.add_argument('--token', required=True, help='JWT access token')
    parser.add_argument('--count', type=int, default=100, help='Number of simultaneous connections')
    parser.add_argument('--duration', type=int, default=10, help='Hold duration in seconds')
    args = parser.parse_args()

    print(f"Load test: {args.count} connections × {args.duration}s  →  {args.url}")

    stats = asyncio.run(_run(args.url, args.token, args.count, args.duration))

    total_errors = stats['err_4001'] + stats['err_refused'] + stats['err_timeout'] + stats['err_other']
    connect_ms = stats['connect_ms']

    print("\n=== Report ===")
    print(f"Attempted connections  : {args.count}")
    print(f"Successful             : {stats['success']}")
    print(f"Errors                 : {total_errors}")
    print(f"  Code 4001 (auth)     : {stats['err_4001']}")
    print(f"  Connection refused   : {stats['err_refused']}")
    print(f"  Timeout              : {stats['err_timeout']}")
    print(f"  Other                : {stats['err_other']}")
    print(f"Messages received      : {stats['messages']}")

    if connect_ms:
        print(f"Avg connect time       : {statistics.mean(connect_ms):.1f} ms")
        print(f"Max latency            : {max(connect_ms):.1f} ms")
    else:
        print("No successful connections — latency data unavailable.")


if __name__ == '__main__':
    main()
