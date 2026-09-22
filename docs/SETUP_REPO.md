# SETUP_REPO: inicializar el repositorio

> **Para el agente de Modelo, en su computadora, el día D1.** Seguí este archivo paso a paso. **Antes de cada paso que cree o modifique algo en GitHub, mostrale al usuario el comando y esperá su confirmación.** Al final hay una sección para el integrante Datos.

---

## Paso 0. Punto de partida

El usuario tiene una carpeta con los archivos del kit:

```
AGENTS.md
README.md
spec.md
docs/SETUP_REPO.md        (este archivo)
docs/CARRIL_MODELO.md
docs/CARRIL_DATOS.md
docs/plan.html
docs/final-project.html   (lo agrega el usuario: consignas del profesor)
```

1. Leé `AGENTS.md` completo.
2. Leé `docs/final-project.html`. **Si no está, pedíselo al usuario antes de seguir.**
3. Buscá en `final-project.html` todo lo que afecte la inicialización: nombre o visibilidad del repo, estructura obligatoria, lenguaje, herramienta del informe, licencia, a quién hay que dar acceso. **Si algo contradice este archivo, gana `final-project.html`.** Resumile al usuario las diferencias antes de crear nada.

## Paso 1. Verificar herramientas

```bash
git --version
gh --version && gh auth status      # GitHub CLI autenticado
python3 --version                   # 3.10 o superior
uv --version                        # recomendado; si no está, ver abajo
```

- Si `gh` no está autenticado, pedile al usuario que corra `gh auth login`.
- Si `uv` no está, ofrecé instalarlo (https://docs.astral.sh/uv/). Si el usuario prefiere no hacerlo, usá `python -m venv .venv` con un `requirements.txt` de versiones fijadas (ver Paso 4).
- Si la computadora es Windows, adaptá los comandos y avisá.

## Paso 2. Pedirle al usuario los datos que faltan

- **Nombre del repo.** Sugerencia: `sirenas-oscuras-h0`.
- **Visibilidad.** Privado, salvo que `final-project.html` pida público.
- **Usuario de GitHub del compañero (Datos)**, para invitarlo.
- **Iniciales de ambos**, para nombrar los archivos de decisiones.

## Paso 3. Estructura de carpetas

Creá esta estructura. Cada `__init__.py` lleva un docstring de una línea que diga quién es dueño del paquete.

```
.
├── AGENTS.md
├── CLAUDE.md                  # una sola línea: @AGENTS.md
├── README.md
├── spec.md
├── pyproject.toml             # lo crea el Paso 4
├── .gitignore
├── .python-version            # lo crea el Paso 4
├── docs/
│   ├── final-project.html
│   ├── plan.html
│   ├── SETUP_REPO.md
│   ├── CARRIL_MODELO.md
│   └── CARRIL_DATOS.md
├── src/sirenas/
│   ├── __init__.py
│   ├── core/__init__.py       # "Código compartido. Dueño: Modelo. No reimplementar: importar."
│   ├── model/__init__.py      # "Likelihoods sintéticas y mezcla. Dueño: Modelo."
│   ├── data/__init__.py       # "Datos reales y reweighting. Dueño: Datos."
│   └── catalogs/__init__.py   # "Catálogos sintéticos y detección. Dueño: Datos."
├── tests/
│   └── test_smoke.py          # importa sirenas y sus cuatro subpaquetes
├── notes/README.md            # derivaciones (una por archivo o LaTeX)
├── configs/.gitkeep
├── scripts/.gitkeep
├── results/.gitkeep
├── figures/.gitkeep
├── provenance/README.md       # plantilla, ver abajo
├── decisiones/README.md       # plantilla, ver abajo
├── validacion/registro_supervision.md   # plantilla, ver abajo
└── report/.gitkeep
```

`CLAUDE.md` contiene solamente:

```
@AGENTS.md
```

Así Claude Code carga `AGENTS.md`, y otros agentes lo leen directo.

**`.gitignore`, como mínimo:**

```
.venv/
__pycache__/
*.pyc
.pytest_cache/
.ipynb_checkpoints/
data/raw/
*.hdf5
*.h5
.DS_Store
```

**`decisiones/README.md`:**

```markdown
# Decisiones

Un archivo por decisión: `AAAA-MM-DD-iniciales-tema.md`. Nunca un archivo único.

## Plantilla
- **Decisión:**
- **Alternativas consideradas:**
- **Por qué:**
- **Quién la tomó / aprobó:**
- **Afecta a:** (archivos, experimentos)
```

**`validacion/registro_supervision.md`:**

```markdown
# Registro de supervisión del agente

Cada error del agente detectado por un humano. Tres líneas por entrada, en el momento. Es material de la presentación.

| Fecha | Carril | Qué hizo mal el agente | Cómo se detectó (control / lectura / intuición) | Gravedad (baja / media / alta) | Qué se hizo |
|---|---|---|---|---|---|
```

**`provenance/README.md`:**

```markdown
# Procedencia

Un archivo por insumo externo, con: URL y DOI · fecha de descarga · SHA-256 · columnas usadas y unidades · prior con que se generaron las muestras (si aplica) · script que lo descarga y scripts que lo consumen.
```

**`notes/README.md`:** una línea que explique que acá van las derivaciones y quién hace cada una, según `AGENTS.md` §16.

## Paso 4. Entorno reproducible

**Con `uv`:**

```bash
uv init --lib --name sirenas --no-readme --vcs none   # respeta src/sirenas/ y README.md existentes; --vcs none porque git se inicializa en el Paso 6
uv add numpy scipy h5py pandas matplotlib pyyaml
uv add --dev pytest
uv lock
```

Fijá la versión de Python en `.python-version`, con la que esté instalada (3.10 o superior). Verificá que `pyproject.toml` declare el paquete en `src/sirenas`.

**Sin `uv`:** primero escribí un `pyproject.toml` mínimo (build-backend `setuptools`, paquete `sirenas` en `src/`, `requires-python` con la versión instalada). Después:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install numpy scipy h5py pandas matplotlib pyyaml pytest
pip freeze > requirements.txt
pip install -e .
```

Después:

```bash
uv run pytest        # o: pytest
```

El smoke test tiene que pasar.

**No agregues dependencias para el informe o las slides todavía.** Se deciden según `final-project.html` (AGENTS.md §19).

## Paso 5. Primera decisión registrada

Creá `decisiones/AAAA-MM-DD-<iniciales>-reparto-y-referencia-sintetica.md`, con la plantilla, que documente:

- El reparto por perfil (Modelo / Datos) en lugar de A brillante / B oscura, y por qué (AGENTS.md §13).
- Que la sirena brillante de referencia es sintética y que GW170817 real es solo validación (AGENTS.md §7).
- El recorte a diez días (AGENTS.md §4).

Aprobado por: los dos integrantes.

## Paso 6. Git y GitHub

**Mostrale cada comando al usuario antes de correrlo.**

```bash
git init -b main
git add .
git commit -m "Inicializa estructura del proyecto, contexto y reparto de carriles"
gh repo create <nombre> --private --source=. --remote=origin --push
#   usar --public en lugar de --private si final-project.html lo pide
```

Invitá al compañero:

```bash
gh api -X PUT repos/<owner>/<nombre>/collaborators/<usuario-datos> -f permission=push
```

**Protección de ramas:** no la configures. En repos privados de cuentas gratuitas de GitHub puede no estar disponible. La regla de «PR revisado por el otro» es una convención del equipo (AGENTS.md §12).

**Opcional (preguntale al usuario):**
- Crear las etiquetas `modelo`, `datos` y `ambos`.
- Crear un issue por cada tarea del plan de diez días (AGENTS.md §14), con su etiqueta.

Sirve para que el agente de cada integrante vea sus tareas con `gh issue list --label <carril>`.

## Paso 7. Verificar desde cero

En un directorio temporal:

```bash
gh repo clone <owner>/<nombre> /tmp/verif-sirenas
cd /tmp/verif-sirenas
uv sync && uv run pytest      # o: venv + pip install -r requirements.txt + pip install -e . + pytest
```

Si falla, arreglalo en el repo original, commiteá y volvé a verificar. Después borrá el directorio temporal.

## Paso 8. Reporte al usuario

Decile al usuario:

- La URL del repo.
- Si la invitación al compañero salió bien.
- Qué se creó.
- Cualquier diferencia con `final-project.html` que hayas tenido que resolver.
- El próximo paso: pasarle al compañero la sección siguiente de este archivo.

---

## Para el integrante Datos: clonar y empezar

1. **Aceptá la invitación** de GitHub (llega por mail, o entrá a https://github.com/notifications).
2. **Cloná y armá el entorno:**

   ```bash
   gh repo clone <owner>/<nombre>          # o: git clone https://github.com/<owner>/<nombre>.git
   cd <nombre>
   uv sync && uv run pytest                 # o: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && pip install -e . && pytest
   ```

   Si no tenés `uv`, instalalo (https://docs.astral.sh/uv/) o usá la alternativa con `venv`.
3. **Abrí tu agente dentro de la carpeta del repo** y mandale el primer mensaje sugerido en `docs/CARRIL_DATOS.md`.
4. **Flujo de trabajo diario:**

   ```bash
   git switch main && git pull
   git switch -c datos/<tema>               # ej.: datos/descarga
   # ... trabajo ...
   git add -A && git commit -m "<qué y por qué>"
   git push -u origin datos/<tema>
   gh pr create --fill --base main          # Modelo lo revisa y lo mergea
   ```

5. **`docs/plan.html`** se abre con doble clic en el navegador. Es la versión visual del plan, el reparto y la bibliografía.
