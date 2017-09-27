import os

if os.environ['is_ai'] == 1:
    import toontown.ai.ServiceStart
if os.environ['is_ud'] == 1:
    import toontown.uberdog.ServiceStart
else:
    import toontown.toonbase.ClientStart