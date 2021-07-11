# pylint: disable=missing-function-docstring,missing-module-docstring,missing-class-docstring,unused-wildcard-import,wildcard-import


__all__ = [
    "BUNDLE_RAW_PART",
    "BUNDLE_CMS_PART",
    "BUNDLE",
    "INVALID_CMS",
    "VALID_CMS_WITH_LENGTH",
]


from base64 import b64decode


BUNDLE_RAW_PART: bytes = b64decode(b"UkFVQyBidW5kbGUK")

BUNDLE_CMS_PART: bytes = b64decode(
    b"\
MIIGagYJKoZIhvcNAQcCoIIGWzCCBlcCAQExDTALBglghkgBZQMEAgEwCwYJKoZIhvcNAQcBoIIE\
DjCCBAowggHyAgEBMA0GCSqGSIb3DQEBCwUAMIGMMQswCQYDVQQGEwJGUjEUMBIGA1UECAwLUmhv\
bmUtQXBsZXMxETAPBgNVBAcMCEdyZW5vYmxlMQ8wDQYDVQQKDAZKYXJzb3AxDzANBgNVBAsMBnJh\
dWNreTEPMA0GA1UEAwwGSmFyc29wMSEwHwYJKoZIhvcNAQkBFhJqYXJzb3BAaG90bWFpbC5jb20w\
HhcNMjEwNzEwMTMwNDA3WhcNMjEwODA5MTMwNDA3WjCBjDELMAkGA1UEBhMCRlIxFDASBgNVBAgM\
C1Job25lLUFscGVzMREwDwYDVQQHDAhHcmVub2JsZTEPMA0GA1UECgwGSmFyc29wMQ8wDQYDVQQL\
DAZyYXVja3kxDzANBgNVBAMMBkphcnNvcDEhMB8GCSqGSIb3DQEJARYSamFyc29wQGhvdG1haWwu\
Y29tMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDNNXLetH1Bc+i/G7iou0WDWmqSfQLlN/MX\
LHpOCVqSfJB9u3HrdLzRLJv0Cu3VVtyMImwo4HXjQTEZvrX2Rt+OFtQTvoHTzUBrGUs4j2m2cnM+\
HpZvsMRriTEf+UnBL4Xnkd218iYhTONlYRKliX5wfG7GxVcn2bKSfsiL2G16AwIDAQABMA0GCSqG\
SIb3DQEBCwUAA4ICAQCIrubgdgW5nXWl11ki3GTHLe4s/+7xzkmpwcswr0bmNgIRnE38SXRUVR9r\
nwXB6tbLxw6JlGIxRkMU3xEk/z5BtNE76XgRGRoZA+01LG8wcXT0JRWr12rGuBJwP5pztTSKJOtW\
ae+qZfQexdrs8Sjp8ImWF6mSrbnd7GmAGLsn+awgKL+ihr3mv0qgWX15ga757l6nKqdNFEFkKohj\
Ph2gsGckblTISL6oPzp+J5MsbEqgH24inQoor8Lt+rZcarCE24v5AhfRb24acqHXoaBv46xSNlWp\
ZnnciwEZQvETjshzzrKAZUSth4B6PjuEZcbEqhF4g3gQ6hktAVZttm1M5qouACwGpDhTjAOTmERa\
EJ0/5mC+T2hdr0KNWnHsSgIxLefy0J6LPg8zO1I5XlO+8QDGiDTPkBVHjou8q66Eu8gS/SYicbCC\
W3hi1lqzlwK1kaEhO9JTZUZRnEQiSKFf7dEkw924IqAPVLA1btpMu8UFsmt8Hbvt3WxuZx2mOXBv\
pfOAKmxWti+wQUPkaeLlsrLV95+RTbGRu9AoChNBv39/myj//NuCthyMibD2Nrf2lcwR5OIeG7Kg\
T/MG/bmfXjNW72xBMD7ZXWBfXRka1MzRT47vobZyJjwpGcQTtifAZBT/a1pPotGHlJY9og+J88qj\
RRwb68hrlYUHZnVChzGCAiIwggIeAgEBMIGSMIGMMQswCQYDVQQGEwJGUjEUMBIGA1UECAwLUmhv\
bmUtQXBsZXMxETAPBgNVBAcMCEdyZW5vYmxlMQ8wDQYDVQQKDAZKYXJzb3AxDzANBgNVBAsMBnJh\
dWNreTEPMA0GA1UEAwwGSmFyc29wMSEwHwYJKoZIhvcNAQkBFhJqYXJzb3BAaG90bWFpbC5jb20C\
AQEwCwYJYIZIAWUDBAIBoIHkMBgGCSqGSIb3DQEJAzELBgkqhkiG9w0BBwEwHAYJKoZIhvcNAQkF\
MQ8XDTIxMDcxMTAwMjcxMlowLwYJKoZIhvcNAQkEMSIEIMIA2eUB3TdV2RsdZhD8kP86d4cMqXHf\
dMviJXzeqCRbMHkGCSqGSIb3DQEJDzFsMGowCwYJYIZIAWUDBAEqMAsGCWCGSAFlAwQBFjALBglg\
hkgBZQMEAQIwCgYIKoZIhvcNAwcwDgYIKoZIhvcNAwICAgCAMA0GCCqGSIb3DQMCAgFAMAcGBSsO\
AwIHMA0GCCqGSIb3DQMCAgEoMA0GCSqGSIb3DQEBAQUABIGAqGVt410b8dW3hhuYybeCcRLlUtU2\
LsqHldfen+o7QmcUy8CiN/2igExA2aaatqErsdu7roEfVDXQzb1huLYNdpDcCkVTszd19PusNY6Y\
lucNgvIiL8EWNiwiMYqMDh2qFZDQ8k08upHa5w2D2kKS9rAOGE8xIBjDCND1KVwtCsM=\
"
)

BUNDLE: bytes = b64decode(
    b"\
UkFVQyBidW5kbGUKMIIGagYJKoZIhvcNAQcCoIIGWzCCBlcCAQExDTALBglghkgBZQMEAgEwCwYJ\
KoZIhvcNAQcBoIIEDjCCBAowggHyAgEBMA0GCSqGSIb3DQEBCwUAMIGMMQswCQYDVQQGEwJGUjEU\
MBIGA1UECAwLUmhvbmUtQXBsZXMxETAPBgNVBAcMCEdyZW5vYmxlMQ8wDQYDVQQKDAZKYXJzb3Ax\
DzANBgNVBAsMBnJhdWNreTEPMA0GA1UEAwwGSmFyc29wMSEwHwYJKoZIhvcNAQkBFhJqYXJzb3BA\
aG90bWFpbC5jb20wHhcNMjEwNzEwMTMwNDA3WhcNMjEwODA5MTMwNDA3WjCBjDELMAkGA1UEBhMC\
RlIxFDASBgNVBAgMC1Job25lLUFscGVzMREwDwYDVQQHDAhHcmVub2JsZTEPMA0GA1UECgwGSmFy\
c29wMQ8wDQYDVQQLDAZyYXVja3kxDzANBgNVBAMMBkphcnNvcDEhMB8GCSqGSIb3DQEJARYSamFy\
c29wQGhvdG1haWwuY29tMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDNNXLetH1Bc+i/G7io\
u0WDWmqSfQLlN/MXLHpOCVqSfJB9u3HrdLzRLJv0Cu3VVtyMImwo4HXjQTEZvrX2Rt+OFtQTvoHT\
zUBrGUs4j2m2cnM+HpZvsMRriTEf+UnBL4Xnkd218iYhTONlYRKliX5wfG7GxVcn2bKSfsiL2G16\
AwIDAQABMA0GCSqGSIb3DQEBCwUAA4ICAQCIrubgdgW5nXWl11ki3GTHLe4s/+7xzkmpwcswr0bm\
NgIRnE38SXRUVR9rnwXB6tbLxw6JlGIxRkMU3xEk/z5BtNE76XgRGRoZA+01LG8wcXT0JRWr12rG\
uBJwP5pztTSKJOtWae+qZfQexdrs8Sjp8ImWF6mSrbnd7GmAGLsn+awgKL+ihr3mv0qgWX15ga75\
7l6nKqdNFEFkKohjPh2gsGckblTISL6oPzp+J5MsbEqgH24inQoor8Lt+rZcarCE24v5AhfRb24a\
cqHXoaBv46xSNlWpZnnciwEZQvETjshzzrKAZUSth4B6PjuEZcbEqhF4g3gQ6hktAVZttm1M5qou\
ACwGpDhTjAOTmERaEJ0/5mC+T2hdr0KNWnHsSgIxLefy0J6LPg8zO1I5XlO+8QDGiDTPkBVHjou8\
q66Eu8gS/SYicbCCW3hi1lqzlwK1kaEhO9JTZUZRnEQiSKFf7dEkw924IqAPVLA1btpMu8UFsmt8\
Hbvt3WxuZx2mOXBvpfOAKmxWti+wQUPkaeLlsrLV95+RTbGRu9AoChNBv39/myj//NuCthyMibD2\
Nrf2lcwR5OIeG7KgT/MG/bmfXjNW72xBMD7ZXWBfXRka1MzRT47vobZyJjwpGcQTtifAZBT/a1pP\
otGHlJY9og+J88qjRRwb68hrlYUHZnVChzGCAiIwggIeAgEBMIGSMIGMMQswCQYDVQQGEwJGUjEU\
MBIGA1UECAwLUmhvbmUtQXBsZXMxETAPBgNVBAcMCEdyZW5vYmxlMQ8wDQYDVQQKDAZKYXJzb3Ax\
DzANBgNVBAsMBnJhdWNreTEPMA0GA1UEAwwGSmFyc29wMSEwHwYJKoZIhvcNAQkBFhJqYXJzb3BA\
aG90bWFpbC5jb20CAQEwCwYJYIZIAWUDBAIBoIHkMBgGCSqGSIb3DQEJAzELBgkqhkiG9w0BBwEw\
HAYJKoZIhvcNAQkFMQ8XDTIxMDcxMTAwMjcxMlowLwYJKoZIhvcNAQkEMSIEIMIA2eUB3TdV2Rsd\
ZhD8kP86d4cMqXHfdMviJXzeqCRbMHkGCSqGSIb3DQEJDzFsMGowCwYJYIZIAWUDBAEqMAsGCWCG\
SAFlAwQBFjALBglghkgBZQMEAQIwCgYIKoZIhvcNAwcwDgYIKoZIhvcNAwICAgCAMA0GCCqGSIb3\
DQMCAgFAMAcGBSsOAwIHMA0GCCqGSIb3DQMCAgEoMA0GCSqGSIb3DQEBAQUABIGAqGVt410b8dW3\
hhuYybeCcRLlUtU2LsqHldfen+o7QmcUy8CiN/2igExA2aaatqErsdu7roEfVDXQzb1huLYNdpDc\
CkVTszd19PusNY6YlucNgvIiL8EWNiwiMYqMDh2qFZDQ8k08upHa5w2D2kKS9rAOGE8xIBjDCND1\
KVwtCsMAAAAAAAAGbg==\
"
)

INVALID_CMS: bytes = b64decode(
    b"\
MIIGagYJKoZIhvcNAQcCoIIGWzCCBlcCAQExDTALBglghkgBZQMEAgEwCwYJKoZIhvcNAQcBoIIE\
DjCCBAowggHyAgEBMA0GCSqGSIb3DQEBCwUAMIGMMQswCQYDVQQGEwJGUjEUMBIGA1UECAwLUmhv\
bmUtQXBsZXMxETAPBgNVBAcMCEdyZW5vYmxlMQ8wDQYDVQQKDAZKYXJzb3AxDzANBgNVBAsMBnJh\
dWNreTEPMA0GA1UEAwwGSmFyc29wMSEwHwYJKoZIhvcNAQkBFhJqYXJzb3BAaG90bWFpbC5jb20w\
HhcNMjEwNzEwMTMwNDA3WhcNMjEwODA5MTMwNDA3WjCBjDELMAkGA1UEBhMCRlIxFDASBgNVBAgM\
C1Job25lLUFscGVzMREwDwYDVQQHDAhHcmVub2JsZTEPMA0GA1UECgwGSmFyc29wMQ8wDQYDVQQL\
DAZyYXVja3kxDzANBgNVBAMMBkphcnNvcDEhMB8GCSqGSIb3DQEJARYSamFyc29wQGhvdG1haWwu\
Y29tMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDNNXLetH1Bc+i/G7iou0WDWmqSfQLlN/MX\
LHpOCVqSfJB9u3HrdLzRLJv0Cu3VVtyMImwo4HXjQTEZvrX2Rt+OFtQTvoHTzUBrGUs4j2m2cnM+\
HpZvsMRriTEf+UnBL4Xnkd218iYhTONlYRKliX5wfG7GxVcn2bKSfsiL2G16AwIDAQABMA0GCSqG\
SIb3DQEBCwUAA4ICAQCIrubgdgW5nXWl11ki3GTHLe4s/+7xzkmpwcswr0bmNgIRnE38SXRUVR9r\
nwXB6tbLxw6JlGIxRkMU3xEk/z5BtNE76XgRGRoZA+01LG8wcXT0JRWr12rGuBJwP5pztTSKJOtW\
ae+qZfQexdrs8Sjp8ImWF6mSrbnd7GmAGLsn+awgKL+ihr3mv0qgWX15ga757l6nKqdNFEFkKohj\
Ph2gsGckblTISL6oPzp+J5MsbEqgH24inQoor8Lt+rZcarCE24v5AhfRb24acqHXoaBv46xSNlWp\
ZnnciwEZQvETjshzzrKAZUSth4B6PjuEZcbEqhF4g3gQ6hktAVZttm1M5qouACwGpDhTjAOTmERa\
EJ0/5mC+T2hdr0KNWnHsSgIxLefy0J6LPg8zO1I5XlO+8QDGiDTPkBVHjou8q66Eu8gS/SYicbCC\
W3hi1lqzlwK1kaEhO9JTZUZRnEQiSKFf7dEkw924IqAPVLA1btpMu8UFsmt8Hbvt3WxuZx2mOXBv\
pfOAKmxWti+wQUPkaeLlsrLV95+RTbGRu9AoChNBv39/myj//NuCthyMibD2Nrf2lcwR5OIeG7Kg\
T/MG/bmfXjNW72xBMD7ZXWBfXRka1MzRT47vobZyJjwpGcQTtifAZBT/a1pPotGHlJY9og+J88qj\
RRwb68hrlYUHZnVChzGCAiIwggIeAgEBMIGSMIGMMQswCQYDVQQGEwJGUjEUMBIGA1UECAwLUmhv\
bmUtQXBsZXMxETAPBgNVBAcMCEdyZW5vYmxlMQ8wDQYDVQQKDAZKYXJzb3AxDzANBgNVBAsMBnJh\
dWNreTEPMA0GA1UEAwwGSmFyc29wMSEwHwYJKoZIhvcNAQkBFhJqYXJzb3BAaG90bWFpbC5jb20C\
AQEwCwYJYIZIAWUDBAIBoIHkMBgGCSqGSIb3DQEJAzELBgkqhkiG9w0BBwEwHAYJKoZIhvcNAQkF\
MQ8XDTIxMDcxMTAwMjcxMlowLwYJKoZIhvcNAQkEMSIEIMIA2eUB3TdV2RsdZhD8kP86d4cMqXHf\
dMviJXzeqCRbMHkGCSqGSIb3DQEJDzFsMGowCwYJYIZIAWUDBAEqMAsGCWCGSAFlAwQBFjALBglg\
hkgBZQMEAQIwCgYIKoZIhvcNAwcwDgYIKoZIhvcNAwICAgCAMA0GCCqGSIb3DQMCAgFAMAcGBSsO\
AwIHMA0GCCqGSIb3DQMCAgEoMA0GCSqGSIb3DQEBAQUABIGAqGVt410b8dW3hhuYybeCcRLlUtU2\
lucNgvIiL8EWNiwiMYqMDh2qFZDQ8k08upHa5w2D2kKS9rAOGE8xIBjDCND1KVwtCsM=\
"
)

VALID_CMS_WITH_LENGTH: bytes = b64decode(
    b"\
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\
bg==\
"
)