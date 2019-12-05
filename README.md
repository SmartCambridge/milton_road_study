The Plan
========

On Tuesday 12 November 2019 the scope of this study was redefined to
look just at a year's worth of inbound traffic on the section of Milton
Road between the A14 junction and its junction with Arbury Rd/Union Lane
during the morning peak (defined to be 07:30-09:30) Monday to Friday.

This corresponds to:

* Drakewell links
    * '36 Milton InB \*\*' (CAMBRIDGE_JTMS|9800X7003HZY - A14 to Green End Rd/Kings Hedges Rd)
    * '12 Milton Rd InB \*' (CAMBRIDGE_JTMS|9800YU0FYRKZ - Green End Rd/Kings
      Hedges Rd to Arbury Rd/Union Ln
    * Combied length 2186m
* (new) SmartCambridge zone:
    * milton\_road\_alternate\_in.

```
    {
      "id": "CAMBRIDGE_JTMS|9800X7003HZY",
      "name": "36 Milton InB **",
      "description": "MACSSL210023 to MACSSL208512",
      "sites": [
        "{32E0BCF3-4F0F-4F5A-9FDA-E7F9DC37B1D3}",
        "{ABD3D082-B375-4EFC-AC05-D7FDED3AB22A}"
      ],
      "length": 1125
    }

    {
      "id": "CAMBRIDGE_JTMS|9800YU0FYRKZ",
      "name": "12 Milton Rd InB *",
      "description": "MACSSL208512 to MACSSL208513",
      "sites": [
        "{ABD3D082-B375-4EFC-AC05-D7FDED3AB22A}",
        "{FC9EAC00-9BAA-4A8E-861A-97531661D3C7}"
      ],
      "length": 1061
    }

    {
      "id": "{32E0BCF3-4F0F-4F5A-9FDA-E7F9DC37B1D3}",
      "name": "Milton Interchange A1304 / A14",
      "description": "Milton Interchange A1304 / A14",
      "location": {
        "lat": 52.23665,
        "lng": 0.15061
      }
    }

    {
      "id": "{ABD3D082-B375-4EFC-AC05-D7FDED3AB22A}",
      "name": "Milton Road / Kings Hedges",
      "description": "Milton Road / Kings Hedges",
      "location": {
        "lat": 52.22752,
        "lng": 0.14536
      }
    }

    {
      "id": "{FC9EAC00-9BAA-4A8E-861A-97531661D3C7}",
      "name": "Milton Road / Union Lane",
      "description": "Milton Road / Union Lane",
      "location": {
        "lat": 52.22075,
        "lng": 0.1343
      }
    }
```
