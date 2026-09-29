"""Perfil agregado (solo conteos) de columnas autorizadas; no imprime filas."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lector_dbf import lee, cabecera  # noqa: E402

for ola in range(2015, 2024):
    h, campos = cabecera(ola)
    df, info = lee(ola)
    print("=====", ola, {k: v for k, v in info.items() if k != "campos"})
    print("  campos autorizados presentes:",
          [(n, t, l) for n, t, l in campos if n in df.columns])
    for c in df.columns:
        vc = df[c].value_counts()
        if c == "CAUSA_DEF":
            print("  CAUSA_DEF vacias:", int((df[c] == "").sum()),
                  "largos:", df[c].str.len().value_counts().to_dict(),
                  "X60-X84:", int(df[c].str[:3].between("X60", "X84").sum()))
        elif c == "EDAD":
            e = df[c]
            print("  EDAD prefijos:", e.str[:1].value_counts().to_dict(),
                  "no-esp:", {k: int(vc.get(k, 0)) for k in ["1098", "2098", "3098", "4998", "1097", "9999", ""]},
                  "largos:", e.str.len().value_counts().to_dict())
        elif len(vc) <= 40:
            print(f"  {c}:", vc.sort_index().to_dict())
        else:
            print(f"  {c}: {len(vc)} valores; min {vc.index.min()} max {vc.index.max()}; top",
                  vc.head(5).to_dict())
