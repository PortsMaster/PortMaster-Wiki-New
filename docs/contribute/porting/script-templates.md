# Standard Portscript Templates

=== "Basic"

    ``` bash
    #!/bin/bash

    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}

    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi

    source $controlfolder/control.txt
    [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"

    get_controls
    GAMEDIR=/$directory/ports/portfolder/
    CONFDIR="$GAMEDIR/conf/"

    mkdir -p "$GAMEDIR/conf"
    cd $GAMEDIR

    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    export XDG_DATA_HOME="$CONFDIR"
    export LD_LIBRARY_PATH="$GAMEDIR/libs.${DEVICE_ARCH}:$LD_LIBRARY_PATH"
    export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"
    bind_directories ~/.portfolder $GAMEDIR/conf/.portfolder

    $GPTOKEYB "portexecutable.${DEVICE_ARCH}" -c "./portname.gptk.$ANALOGSTICKS" &
    pm_platform_helper "$GAMEDIR/portexecutable.${DEVICE_ARCH}"
    ./portexecutable.${DEVICE_ARCH}
    pm_finish
    ```





=== "Godot 3"

    ``` bash
    #!/bin/bash

    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}

    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi

    source $controlfolder/control.txt

    [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"

    get_controls

    GAMEDIR=/$directory/ports/portfolder/
    CONFDIR="$GAMEDIR/conf/"

    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    mkdir -p "$GAMEDIR/conf"
    cd $GAMEDIR

    runtime="frt_3.2.3"
    if [ ! -f "$controlfolder/libs/${runtime}.squashfs" ]; then
      # Check for runtime if not downloaded via PM
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi

      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${runtime}.squashfs"
    fi

    # Set the XDG environment variables for config & savefiles
    export XDG_DATA_HOME="$CONFDIR"
    export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"

    #  If XDG Path does not work
    # Use _directories to reroute that to a location within the ports folder.
    bind_directories ~/.portfolder $GAMEDIR/conf/.portfolder 

    # Setup Godot
    godot_dir="$HOME/godot"
    godot_file="$controlfolder/libs/${runtime}.squashfs"
    $ESUDO mkdir -p "$godot_dir"
    $ESUDO umount "$godot_file" || true
    $ESUDO mount "$godot_file" "$godot_dir"
    PATH="$godot_dir:$PATH"

    # By default FRT sets Select as a Force Quit Hotkey, with this we disable that.
    export FRT_NO_EXIT_SHORTCUTS=FRT_NO_EXIT_SHORTCUTS 


    $GPTOKEYB "$runtime" -c "./godot.gptk" &
    pm_platform_helper "$godot_dir/$runtime"
    "$runtime" $GODOT_OPTS --main-pack "gamename.pck"

    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "$godot_dir"
    fi
    pm_finish
    ```




=== "Love2d"
    ```bash
    #!/bin/bash

    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}

    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi

    source $controlfolder/control.txt

    [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"

    get_controls

    GAMEDIR=/$directory/ports/portfolder
    CONFDIR="$GAMEDIR/conf/"

    mkdir -p "$GAMEDIR/conf"
    cd $GAMEDIR

    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Set the XDG environment variables for config & savefiles
    export XDG_DATA_HOME="$CONFDIR"

    #  If XDG Path does not work
    # Use bind_directories to reroute that to a location within the ports folder.
    bind_directories ~/.portfolder $GAMEDIR/conf/.portfolder 

    export LD_LIBRARY_PATH="$GAMEDIR/libs.${DEVICE_ARCH}:$LD_LIBRARY_PATH"
    export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"

    source $controlfolder/runtimes/"love_11.5"/love.txt

    # Run the love runtime
    $GPTOKEYB "$LOVE_GPTK" &
    pm_platform_helper "$LOVE_BINARY"
    $LOVE_RUN "$GAMEDIR/lovegame"

    pm_finish
    ```




=== "GameMaker"
    ```bash
    #!/bin/bash

    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}

    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi

    export controlfolder

    source $controlfolder/control.txt

    export PORT_32BIT="Y" # If using a 32 bit port
    [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"

    get_controls

    GAMEDIR=/$directory/ports/portfolder/

    cd $GAMEDIR
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    export LD_LIBRARY_PATH="$GAMEDIR/libs.${DEVICE_ARCH}:$LD_LIBRARY_PATH"
    export GMLOADER_DEPTH_DISABLE=1
    export GMLOADER_SAVEDIR="$GAMEDIR/gamedata/"
    export GMLOADER_PLATFORM="os_linux"
    export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"
    $ESUDO chmod +x "$GAMEDIR/gmloader"

    # if no .gptk file is used use $GPTOKEYB "gmloader" & 
    $GPTOKEYB "gmloader" -c ./controls.gptk &
    pm_platform_helper "gmloader"
    ./gmloader donor.apk

    pm_finish
    ```




=== "Pyxel"
    ```bash
    #!/bin/bash

    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}

    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi

    source $controlfolder/control.txt

    [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"

    get_controls

    GAMEDIR=/$directory/ports/portfolder/
    CONFDIR="$GAMEDIR/conf"
    PYXEL_PKG="gamename.pyxapp"

    cd "${GAMEDIR}"

    > "${GAMEDIR}/log.txt" && exec > >(tee "${GAMEDIR}/log.txt") 2>&1

    mkdir -p "$GAMEDIR/conf"
    bind_directories "$HOME/.config/.pyxel/gamename" "$CONFDIR"
    # note: replace gamename with the appropriate value for the game

    # Load Pyxel runtime
    runtime="pyxel_2.2.8_python_3.11"
    export pyxel_dir="$HOME/pyxel"
    mkdir -p "${pyxel_dir}"

    if [ ! -f "$controlfolder/libs/${runtime}.squashfs" ]; then
      # Check for runtime if not downloaded via PM
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi

      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${runtime}.squashfs"
    fi

    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${pyxel_dir}"
    fi

    $ESUDO mount "$controlfolder/libs/${runtime}.squashfs" "${pyxel_dir}"

    export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"

    $GPTOKEYB "pyxel" &

    pm_platform_helper "${pyxel_dir}/bin/pyxel"

    # Enable Pyxel virtual env
    source "${pyxel_dir}/bin/activate"
    export PYTHONHOME="${pyxel_dir}"
    export PYTHONPYCACHEPREFIX="${GAMEDIR}/${runtime}.cache"

    # play the pyxel package stored in gamedata
    "${pyxel_dir}/bin/pyxel" play "${GAMEDIR}/gamedata/${PYXEL_PKG}"

    # Alternatively, run a python script file
    # "${pyxel_dir}/bin/pyxel" run gamedata/main.py

    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${pyxel_dir}"
    fi

    pm_finish
    ```




=== "gl4es"

    ``` bash
    #!/bin/bash

    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}

    # PortMaster sits in a different folder on each CFW: these four cover every supported one
    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi

    # control.txt: device info ($DEVICE_ARCH, $CFW_NAME, $DISPLAY_WIDTH, $DEVICE_HAS_ARMHF ...), $ESUDO, $GPTOKEYB2, the pm_* helpers
    source $controlfolder/control.txt
    # mod_<CFW>.txt: the per-CFW fixes PortMaster maintains for every port (no CFW checks needed in the script)
    [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"
    # The device's SDL controller mapping, in $sdl_controllerconfig
    get_controls

    GAMEDIR=/$directory/ports/portfolder
    cd $GAMEDIR

    # Everything the script and the game print ends up in log.txt, the file testers send
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    export LD_LIBRARY_PATH="$GAMEDIR/libs.${DEVICE_ARCH}:$LD_LIBRARY_PATH"
    export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"

    # The CFW's libgl file decides whether gl4es is needed (a device with native GL skips it); source it from $GAMEDIR
    if [ -f "${controlfolder}/libgl_${CFW_NAME}.txt" ]; then
      source "${controlfolder}/libgl_${CFW_NAME}.txt"
    else
      source "${controlfolder}/libgl_default.txt"
    fi
    # Only when gl4es is in use: some engines need its libraries named explicitly
    if [[ ":$LD_LIBRARY_PATH:" == *":$GAMEDIR/gl4es.${DEVICE_ARCH}:"* ]]; then
      export SDL_VIDEO_GL_DRIVER="$GAMEDIR/gl4es.${DEVICE_ARCH}/libGL.so.1"
      export SDL_VIDEO_EGL_DRIVER="$GAMEDIR/gl4es.${DEVICE_ARCH}/libEGL.so.1"
    fi

    $GPTOKEYB2 "portexecutable.${DEVICE_ARCH}" -c "./portexecutable.ini" &
    pm_platform_helper "$GAMEDIR/portexecutable.${DEVICE_ARCH}"
    ./portexecutable.${DEVICE_ARCH}

    pm_finish
    ```

=== "Patcher"

    ``` bash
    #!/bin/bash

    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}

    # PortMaster sits in a different folder on each CFW: these four cover every supported one
    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi

    # control.txt: device info ($DEVICE_ARCH, $CFW_NAME, $DISPLAY_WIDTH, $DEVICE_HAS_ARMHF ...), $ESUDO, $GPTOKEYB2, the pm_* helpers
    source $controlfolder/control.txt
    # mod_<CFW>.txt: the per-CFW fixes PortMaster maintains for every port (no CFW checks needed in the script)
    [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"
    # The device's SDL controller mapping, in $sdl_controllerconfig
    get_controls

    GAMEDIR=/$directory/ports/portfolder
    cd $GAMEDIR

    # Everything the script and the game print ends up in log.txt, the file testers send
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # First launch: PortMaster's patcher runs the port's setup with a progress screen. The script prints
    # "PATCH_FAIL_MSG:<why>" and "Patching process failed!" when it fails; the patcher shows both.
    if [ ! -f "$GAMEDIR/.setup_done" ]; then
      export PATCHER_FILE="$GAMEDIR/tools/patchscript"
      export PATCHER_GAME="<Game>"
      export PATCHER_TIME="a few minutes"
      chmod +x "$PATCHER_FILE"
      source "$controlfolder/utils/patcher.txt"
      cd $GAMEDIR
    fi
    if [ ! -f "$GAMEDIR/.setup_done" ]; then
      pm_message "<Game> is not set up yet: copy your game files into ports/portfolder/gamedata and launch again (log: patchlog.txt)."
      sleep 5
      pm_finish
      exit 1
    fi

    export LD_LIBRARY_PATH="$GAMEDIR/libs.${DEVICE_ARCH}:$LD_LIBRARY_PATH"
    export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"
    $GPTOKEYB2 "portexecutable.${DEVICE_ARCH}" &
    pm_platform_helper "$GAMEDIR/portexecutable.${DEVICE_ARCH}"
    ./portexecutable.${DEVICE_ARCH}

    pm_finish
    ```

=== "gmloader-next"

    ``` bash
    #!/bin/bash

    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}

    # PortMaster sits in a different folder on each CFW: these four cover every supported one
    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi

    # control.txt: device info ($DEVICE_ARCH, $CFW_NAME, $DISPLAY_WIDTH, $DEVICE_HAS_ARMHF ...), $ESUDO, $GPTOKEYB2, the pm_* helpers
    source $controlfolder/control.txt
    # mod_<CFW>.txt: the per-CFW fixes PortMaster maintains for every port (no CFW checks needed in the script)
    [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"
    # The device's SDL controller mapping, in $sdl_controllerconfig
    get_controls

    GAMEDIR=/$directory/ports/portfolder
    cd $GAMEDIR

    # Everything the script and the game print ends up in log.txt, the file testers send
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # gmloader-next (aarch64) runs the game's Android data; gmloader.json names the APK/data and the save folder
    export LD_LIBRARY_PATH="/usr/lib:$GAMEDIR/lib:$LD_LIBRARY_PATH"
    export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"
    $ESUDO chmod +x "$GAMEDIR/gmloadernext.aarch64"

    $GPTOKEYB2 "gmloadernext.aarch64" -c "./game.ini" &
    pm_platform_helper "$GAMEDIR/gmloadernext.aarch64"
    ./gmloadernext.aarch64 -c gmloader.json

    pm_finish
    ```

=== "mkxp-z"

    ``` bash
    #!/bin/bash

    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}

    # PortMaster sits in a different folder on each CFW: these four cover every supported one
    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi

    # control.txt: device info ($DEVICE_ARCH, $CFW_NAME, $DISPLAY_WIDTH, $DEVICE_HAS_ARMHF ...), $ESUDO, $GPTOKEYB2, the pm_* helpers
    source $controlfolder/control.txt
    # mod_<CFW>.txt: the per-CFW fixes PortMaster maintains for every port (no CFW checks needed in the script)
    [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"
    # The device's SDL controller mapping, in $sdl_controllerconfig
    get_controls

    GAMEDIR=/$directory/ports/portfolder
    cd $GAMEDIR

    # Everything the script and the game print ends up in log.txt, the file testers send
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # mkxp-z runs the RPG Maker XP/VX/VX Ace game; mkxp.json next to it points at the game folder
    export LD_LIBRARY_PATH="$GAMEDIR/libs.${DEVICE_ARCH}:$LD_LIBRARY_PATH"
    export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"

    $GPTOKEYB2 "mkxp-z.${DEVICE_ARCH}" -c "./game.ini" &
    pm_platform_helper "$GAMEDIR/mkxp-z.${DEVICE_ARCH}"
    ./mkxp-z.${DEVICE_ARCH}

    pm_finish
    ```

=== "Ren'Py"

    ``` bash
    #!/bin/bash

    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}

    # PortMaster sits in a different folder on each CFW: these four cover every supported one
    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi

    # control.txt: device info ($DEVICE_ARCH, $CFW_NAME, $DISPLAY_WIDTH, $DEVICE_HAS_ARMHF ...), $ESUDO, $GPTOKEYB2, the pm_* helpers
    source $controlfolder/control.txt
    # mod_<CFW>.txt: the per-CFW fixes PortMaster maintains for every port (no CFW checks needed in the script)
    [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"
    # The device's SDL controller mapping, in $sdl_controllerconfig
    get_controls

    GAMEDIR=/$directory/ports/portfolder
    cd $GAMEDIR

    # Everything the script and the game print ends up in log.txt, the file testers send
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Ren'Py runtime from PortMaster (listed in port.json's "runtime")
    runtime="renpy_8.3.4"
    if [ ! -f "$controlfolder/libs/${runtime}.squashfs" ]; then
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${runtime}.squashfs"
    fi
    renpydir="$GAMEDIR/renpy"
    $ESUDO mkdir -p "$renpydir"
    $ESUDO umount "$renpydir" 2>/dev/null
    $ESUDO mount "$controlfolder/libs/${runtime}.squashfs" "$renpydir"

    # Ren'Py keeps saves in ~/.renpy
    mkdir -p "$GAMEDIR/conf"
    bind_directories ~/.renpy "$GAMEDIR/conf"

    export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"
    export PYTHONHOME="$renpydir"
    export PYTHONPATH="$renpydir/lib/python3.9"
    if [ -f "${controlfolder}/libgl_${CFW_NAME}.txt" ]; then
      source "${controlfolder}/libgl_${CFW_NAME}.txt"
    else
      source "${controlfolder}/libgl_default.txt"
    fi

    $GPTOKEYB2 "startRENPY" -c "./game.ini" &
    pm_platform_helper "$renpydir/lib/py3-linux-aarch64/startRENPY"
    "$renpydir/startRENPY" "$GAMEDIR/game"

    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
      $ESUDO umount "$renpydir"
    fi
    pm_finish
    ```

=== "Mono"

    ``` bash
    #!/bin/bash

    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}

    # PortMaster sits in a different folder on each CFW: these four cover every supported one
    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi

    # control.txt: device info ($DEVICE_ARCH, $CFW_NAME, $DISPLAY_WIDTH, $DEVICE_HAS_ARMHF ...), $ESUDO, $GPTOKEYB2, the pm_* helpers
    source $controlfolder/control.txt
    # mod_<CFW>.txt: the per-CFW fixes PortMaster maintains for every port (no CFW checks needed in the script)
    [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"
    # The device's SDL controller mapping, in $sdl_controllerconfig
    get_controls

    GAMEDIR=/$directory/ports/portfolder
    cd "$GAMEDIR/gamedata"

    # Everything the script and the game print ends up in log.txt, the file testers send
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Mono runtime from PortMaster (downloaded with the port when listed in port.json's "runtime")
    monodir="$HOME/mono"
    monofile="$controlfolder/libs/mono-6.12.0.122-aarch64.squashfs"
    if [ ! -f "$monofile" ]; then
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "mono-6.12.0.122-aarch64.squashfs"
    fi
    $ESUDO mkdir -p "$monodir"
    $ESUDO umount "$monofile" || true
    $ESUDO mount "$monofile" "$monodir"

    # Saves live in the port folder
    mkdir -p "$GAMEDIR/savedata"
    bind_directories ~/.local/share/Game "$GAMEDIR/savedata"

    # The game's bundled Windows/old Mono and FNA assemblies lose against the runtime's and the port's newer FNA in dlls/
    rm -f System*.dll mscorlib.dll Mono.*.dll FNA.dll FNA.dll.config

    export MONO_PATH="$GAMEDIR/dlls"
    export LD_LIBRARY_PATH="$GAMEDIR/libs.${DEVICE_ARCH}:$monodir/lib:$LD_LIBRARY_PATH"
    export PATH="$monodir/bin:$PATH"
    export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"
    # FNA3D on the devices' GLES3
    export FNA3D_FORCE_DRIVER=OpenGL
    export FNA3D_OPENGL_FORCE_ES3=1

    $GPTOKEYB2 "mono" &
    pm_platform_helper "$monodir/bin/mono"
    mono Game.exe

    $ESUDO umount "$monodir"
    pm_finish
    ```

=== ".NET 8"

    ``` bash
    #!/bin/bash

    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}

    # PortMaster sits in a different folder on each CFW: these four cover every supported one
    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi

    # control.txt: device info ($DEVICE_ARCH, $CFW_NAME, $DISPLAY_WIDTH, $DEVICE_HAS_ARMHF ...), $ESUDO, $GPTOKEYB2, the pm_* helpers
    source $controlfolder/control.txt
    # mod_<CFW>.txt: the per-CFW fixes PortMaster maintains for every port (no CFW checks needed in the script)
    [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"
    # The device's SDL controller mapping, in $sdl_controllerconfig
    get_controls

    GAMEDIR=/$directory/ports/portfolder
    cd $GAMEDIR

    # Everything the script and the game print ends up in log.txt, the file testers send
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # .NET 8 runtime from PortMaster (listed in port.json's "runtime")
    dotnet_runtime="dotnet-8.0.12"
    if [ ! -f "$controlfolder/libs/${dotnet_runtime}.squashfs" ]; then
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${dotnet_runtime}.squashfs"
    fi
    dotnet_dir=/tmp/dotnet8
    $ESUDO mkdir -p "$dotnet_dir"
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
      $ESUDO umount "$dotnet_dir" 2>/dev/null
    fi
    $ESUDO mount "$controlfolder/libs/${dotnet_runtime}.squashfs" "$dotnet_dir"

    mkdir -p "$GAMEDIR/conf"
    bind_directories ~/.config/Studio/Game "$GAMEDIR/conf"

    cd "$GAMEDIR/gamedata"
    export DOTNET_ROOT="$dotnet_dir"
    export LD_LIBRARY_PATH="$GAMEDIR/libs.${DEVICE_ARCH}:$LD_LIBRARY_PATH"
    export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"
    export FNA3D_FORCE_DRIVER=OpenGL
    export FNA3D_OPENGL_FORCE_ES3=1

    $GPTOKEYB2 "dotnet" &
    pm_platform_helper "$dotnet_dir/dotnet"
    "$dotnet_dir/dotnet" Game.dll

    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
      $ESUDO umount "$dotnet_dir"
    fi
    pm_finish
    ```

=== "box64"

    ``` bash
    #!/bin/bash

    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}

    # PortMaster sits in a different folder on each CFW: these four cover every supported one
    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi

    # control.txt: device info ($DEVICE_ARCH, $CFW_NAME, $DISPLAY_WIDTH, $DEVICE_HAS_ARMHF ...), $ESUDO, $GPTOKEYB2, the pm_* helpers
    source $controlfolder/control.txt
    # mod_<CFW>.txt: the per-CFW fixes PortMaster maintains for every port (no CFW checks needed in the script)
    [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"
    # The device's SDL controller mapping, in $sdl_controllerconfig
    get_controls

    GAMEDIR=/$directory/ports/portfolder
    cd $GAMEDIR

    # Everything the script and the game print ends up in log.txt, the file testers send
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # The player's copy of the game (the x86 Linux build)
    if [ ! -f "$GAMEDIR/gamedata/game.x86_64" ]; then
      pm_message "Copy the Linux version of <Game> into ports/portfolder/gamedata and launch again."
      sleep 5
      pm_finish
      exit 1
    fi
    chmod +x "$GAMEDIR/box64/box64" "$GAMEDIR/gamedata/game.x86_64"

    # box64 hands the game's SDL2 calls to the device's own SDL2. For desktop OpenGL the CFW's libgl file
    # decides whether gl4es is needed (source it from $GAMEDIR, it looks for gl4es.* there)
    if [ -f "${controlfolder}/libgl_${CFW_NAME}.txt" ]; then
      source "${controlfolder}/libgl_${CFW_NAME}.txt"
    else
      source "${controlfolder}/libgl_default.txt"
    fi
    if [ -n "$LIBGL_ES" ]; then
      export SDL_VIDEO_GL_DRIVER="$GAMEDIR/gl4es.aarch64/libGL.so.1"
    fi

    # Native (aarch64) libraries for the calls box64 wraps, x86 libraries the game needs that box64 doesn't wrap
    export LD_LIBRARY_PATH="$GAMEDIR/libs.aarch64:$LD_LIBRARY_PATH"
    export BOX64_LD_LIBRARY_PATH="$GAMEDIR/libs.x86_64"
    export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"

    # Saves and settings in the port folder (the game's own folder in $HOME)
    mkdir -p "$GAMEDIR/conf"
    bind_directories ~/.local/share/Game "$GAMEDIR/conf"

    cd "$GAMEDIR/gamedata"
    $GPTOKEYB2 "game.x86_64" -c "$GAMEDIR/game.ini" &
    pm_platform_helper "$GAMEDIR/box64/box64"
    "$GAMEDIR/box64/box64" ./game.x86_64

    pm_finish
    ```

=== "box86"

    ``` bash
    #!/bin/bash

    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}

    # PortMaster sits in a different folder on each CFW: these four cover every supported one
    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi

    # control.txt: device info ($DEVICE_ARCH, $CFW_NAME, $DISPLAY_WIDTH, $DEVICE_HAS_ARMHF ...), $ESUDO, $GPTOKEYB2, the pm_* helpers
    source $controlfolder/control.txt
    # box86 is a 32-bit (armhf) program: before mod_<CFW>.txt, so it sets up the 32-bit sound libraries
    export PORT_32BIT="Y"
    # mod_<CFW>.txt: the per-CFW fixes PortMaster maintains for every port (no CFW checks needed in the script)
    [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"
    # The device's SDL controller mapping, in $sdl_controllerconfig
    get_controls

    GAMEDIR=/$directory/ports/portfolder
    cd $GAMEDIR

    # Everything the script and the game print ends up in log.txt, the file testers send
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # The player's copy of the game (the x86 Linux build)
    if [ ! -f "$GAMEDIR/gamedata/game.x86" ]; then
      pm_message "Copy the Linux version of <Game> into ports/portfolder/gamedata and launch again."
      sleep 5
      pm_finish
      exit 1
    fi
    chmod +x "$GAMEDIR/box86/box86" "$GAMEDIR/gamedata/game.x86"

    # box86 hands the game's SDL2 calls to the device's own SDL2. For desktop OpenGL the CFW's libgl file
    # decides whether gl4es is needed (source it from $GAMEDIR, it looks for gl4es.* there)
    if [ -f "${controlfolder}/libgl_${CFW_NAME}.txt" ]; then
      source "${controlfolder}/libgl_${CFW_NAME}.txt"
    else
      source "${controlfolder}/libgl_default.txt"
    fi
    if [ -n "$LIBGL_ES" ]; then
      export SDL_VIDEO_GL_DRIVER="$GAMEDIR/gl4es.armhf/libGL.so.1"
    fi

    # Native (armhf) libraries for the calls box86 wraps, x86 libraries the game needs that box86 doesn't wrap
    export LD_LIBRARY_PATH="$GAMEDIR/libs.armhf:/usr/lib32:/usr/lib/arm-linux-gnueabihf:$LD_LIBRARY_PATH"
    export BOX86_LD_LIBRARY_PATH="$GAMEDIR/libs.x86"
    export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"

    # Saves and settings in the port folder (the game's own folder in $HOME)
    mkdir -p "$GAMEDIR/conf"
    bind_directories ~/.local/share/Game "$GAMEDIR/conf"

    cd "$GAMEDIR/gamedata"
    $GPTOKEYB2 "game.x86" -c "$GAMEDIR/game.ini" &
    pm_platform_helper "$GAMEDIR/box86/box86"
    "$GAMEDIR/box86/box86" ./game.x86

    pm_finish
    ```

=== "RPG Maker MV"

    ``` bash
    #!/bin/bash

    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}

    # PortMaster sits in a different folder on each CFW: these four cover every supported one
    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi

    # control.txt: device info ($DEVICE_ARCH, $CFW_NAME, $DISPLAY_WIDTH, $DEVICE_HAS_ARMHF ...), $ESUDO, $GPTOKEYB2, the pm_* helpers
    source $controlfolder/control.txt
    # mod_<CFW>.txt: the per-CFW fixes PortMaster maintains for every port (no CFW checks needed in the script)
    [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"
    # The device's SDL controller mapping, in $sdl_controllerconfig
    get_controls

    GAMEDIR=/$directory/ports/portfolder
    cd $GAMEDIR

    # Everything the script and the game print ends up in log.txt, the file testers send
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # The player's copy: the www/ folder of the RPG Maker MV/MZ game
    if [ ! -f "$GAMEDIR/gamedata/www/index.html" ]; then
      pm_message "Copy the www folder of your copy of <Game> into ports/portfolder/gamedata and launch again."
      sleep 5
      pm_finish
      exit 1
    fi

    export LD_LIBRARY_PATH="$GAMEDIR/libs.${DEVICE_ARCH}:$LD_LIBRARY_PATH"
    export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"
    # quixjs' own launcher menu draws with this font
    export QUIXJS_FONT="$GAMEDIR/fonts/DejaVuSans-Bold.ttf"
    chmod +x "$GAMEDIR/quixjs.${DEVICE_ARCH}"

    # quixjs reads the pad itself: gptokeyb2 only provides the hotkey exit (leave $HOTKEY to control.txt)
    $GPTOKEYB2 "quixjs.${DEVICE_ARCH}" &
    pm_platform_helper "$GAMEDIR/quixjs.${DEVICE_ARCH}"
    ./quixjs.${DEVICE_ARCH} --launcher -c port.toml

    pm_finish
    ```

=== "Unity"

    ``` bash
    #!/bin/bash

    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}

    # PortMaster sits in a different folder on each CFW: these four cover every supported one
    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi

    # control.txt: device info ($DEVICE_ARCH, $CFW_NAME, $DISPLAY_WIDTH, $DEVICE_HAS_ARMHF ...), $ESUDO, $GPTOKEYB2, the pm_* helpers
    source $controlfolder/control.txt

    GAMEDIR=/$directory/ports/portfolder
    cd $GAMEDIR

    # Unity's 32-bit Android player is faster but needs the 32-bit userland with glibc 2.35 or newer;
    # without it the 64-bit build. A build that is set up keeps its route.
    if [ -f .setup_done ]; then ROUTE=32
    elif [ -f .setup_done64 ]; then ROUTE=64
    else
      ROUTE=64
      if [ "$DEVICE_HAS_ARMHF" = Y ]; then
        read -r major minor < <(/lib/ld-linux-armhf.so.3 --version 2>/dev/null | sed -n '1s/.*version \([0-9]*\)\.\([0-9]*\).*/\1 \2/p')
        [ -n "$minor" ] && [ $((major * 1000 + minor)) -ge 2035 ] && ROUTE=32
      fi
    fi
    # Before mod_<CFW>.txt: it then sets up the 32-bit sound libraries (PipeWire in /usr/lib32)
    [ "$ROUTE" = 32 ] && export PORT_32BIT="Y"
    # mod_<CFW>.txt: the per-CFW fixes PortMaster maintains for every port (no CFW checks needed in the script)
    [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"
    # The device's SDL controller mapping, in $sdl_controllerconfig
    get_controls

    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1
    if [ "$ROUTE" = 64 ]; then
      SETUP=patchscript64; READY=.setup_done64; HOST=ua_host64
    else
      SETUP=patchscript; READY=.setup_done; HOST=ua_host
    fi

    # First launch: the setup converts the player's copy (PortMaster's patcher shows the progress)
    if [ ! -f "$READY" ]; then
      export GAMEDIR controlfolder
      export PATCHER_FILE="$GAMEDIR/setup/$SETUP" PATCHER_GAME="<Game>" PATCHER_TIME="up to an hour, once"
      chmod +x "$PATCHER_FILE"
      source "$controlfolder/utils/patcher.txt"
      cd $GAMEDIR
    fi
    if [ ! -f "$READY" ]; then
      pm_message "<Game> is not set up yet: copy your game into ports/portfolder/gamedata and launch again (log: patchlog.txt)."
      sleep 5
      pm_finish
      exit 1
    fi

    export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"
    chmod +x "$HOST"
    # The game reads the pad itself: gptokeyb2 only provides the hotkey exit
    $GPTOKEYB2 "$HOST" &
    pm_platform_helper "$GAMEDIR/$HOST"
    if [ "$ROUTE" = 64 ]; then
      ./ua_host64 "$GAMEDIR/arm64"
    else
      # The 32-bit player's libraries live in /lib32 or /usr/lib32 on CFWs with a 32-bit userland
      LD_LIBRARY_PATH=/lib32:/usr/lib32:$LD_LIBRARY_PATH ./ua_host "$GAMEDIR"
    fi

    pm_finish
    ```

<br>

--- 

# Westonpack Portscript Templates


=== "Godot 4"

    ``` bash
    #!/bin/bash

    # PortMaster preamble
    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}
    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi
    source $controlfolder/control.txt
    [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"
    get_controls

    # Adjust these to your paths and desired godot version
    GAMEDIR=/$directory/ports/your_port_folder
    godot_runtime="godot_4.2.2"
    godot_executable="godot422.$DEVICE_ARCH"
    pck_filename="YourGame.pck"
    gptk_filename="YourControls.gptk"

    # Logging
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Create directory for save files
    CONFDIR="$GAMEDIR/conf/"
    $ESUDO mkdir -p "${CONFDIR}"

    # Mount Weston runtime
    weston_dir=/tmp/weston
    $ESUDO mkdir -p "${weston_dir}"
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    # Mount Godot runtime
    godot_dir=/tmp/godot
    $ESUDO mkdir -p "${godot_dir}"
    if [ ! -f "$controlfolder/libs/${godot_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${godot_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${godot_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${godot_runtime}.squashfs" "${godot_dir}"


    cd $GAMEDIR
    $GPTOKEYB "$godot_executable" -c "$GAMEDIR/$gptk_filename" &

    # Start Westonpack and Godot
    # Put CRUSTY_SHOW_CURSOR=1 after "env" if you need a mouse cursor
    $ESUDO env $weston_dir/westonwrap.sh headless noop kiosk crusty_x11egl \
    XDG_DATA_HOME=$CONFDIR $godot_dir/$godot_executable \
    --resolution ${DISPLAY_WIDTH}x${DISPLAY_HEIGHT} -f \
    --rendering-driver opengl3_es --audio-driver ALSA --main-pack $GAMEDIR/$pck_filename

    #Clean up after ourselves
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
        $ESUDO umount "${godot_dir}"
    fi
    pm_finish
    ```

=== "Java"
    **No GL, pure Xlib:**
    ``` bash 
    #!/bin/bash

    # PortMaster preamble
    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}
    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi
    source $controlfolder/control.txt
    get_controls

    # Adjust these to your paths and desired java version
    GAMEDIR=/$directory/ports/your_port_folder
    java_runtime="zulu17.54.21-ca-jre17.0.13-linux"
    jar_filename="YourGame.jar"
    gptk_filename="YourControls.gptk"

    # Logging
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Create directory for save files
    CONFDIR="$GAMEDIR/conf/"
    $ESUDO mkdir -p "${CONFDIR}"

    # Mount Weston runtime
    weston_dir=/tmp/weston
    $ESUDO mkdir -p "${weston_dir}"
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    # Mount Java runtime
    export JAVA_HOME="/tmp/javaruntime/"
    $ESUDO mkdir -p "${JAVA_HOME}"
    if [ ! -f "$controlfolder/libs/${java_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${java_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${JAVA_HOME}"
    fi
    $ESUDO mount "$controlfolder/libs/${java_runtime}.squashfs" "${JAVA_HOME}"
    export PATH="$JAVA_HOME/bin:$PATH"


    cd $GAMEDIR
    $GPTOKEYB "java" -c "$GAMEDIR/$gptk_filename" &

    # Start Westonpack and Java
    $ESUDO env $weston_dir/westonwrap.sh drm gl kiosk system \
    PATH="$PATH" JAVA_HOME="$JAVA_HOME" XDG_DATA_HOME="$GAMEDIR" WAYLAND_DISPLAY= \
    java -jar $GAMEDIR/$jar_filename

    #Clean up after ourselves
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
        $ESUDO umount "${JAVA_HOME}"
    fi
    pm_finish
    ```



    **OpenGL 2.1, through Mesapack/VirGL:**
    ``` bash 
    #!/bin/bash

    # PortMaster preamble
    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}
    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi
    source $controlfolder/control.txt
    get_controls

    # Adjust these to your paths and desired java version
    GAMEDIR=/$directory/ports/your_port_folder
    java_runtime="zulu17.54.21-ca-jre17.0.13-linux"
    jar_filename="YourGame.jar"
    gptk_filename="YourControls.gptk"

    # Logging
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Create directory for save files
    CONFDIR="$GAMEDIR/conf/"
    $ESUDO mkdir -p "${CONFDIR}"

    # Mount Weston runtime
    weston_dir=/tmp/weston
    $ESUDO mkdir -p "${weston_dir}"
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    # Mount Mesa runtime
    mesa_dir=/tmp/mesa
    $ESUDO mkdir -p "${mesa_dir}"
    mesa_runtime="mesa_pkg_0.1"
    if [ ! -f "$controlfolder/libs/${mesa_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${mesa_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${mesa_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${mesa_runtime}.squashfs" "${mesa_dir}"

    # Mount Java runtime
    export JAVA_HOME="/tmp/javaruntime/"
    $ESUDO mkdir -p "${JAVA_HOME}"
    if [ ! -f "$controlfolder/libs/${java_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${java_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${JAVA_HOME}"
    fi
    $ESUDO mount "$controlfolder/libs/${java_runtime}.squashfs" "${JAVA_HOME}"
    export PATH="$JAVA_HOME/bin:$PATH"


    cd $GAMEDIR
    $GPTOKEYB "java" -c "$GAMEDIR/$gptk_filename" &

    # Start Westonpack and Java
    # Put CRUSTY_SHOW_CURSOR=1 after "env" if you need a mouse cursor
    $ESUDO env $weston_dir/westonwrap.sh drm gl kiosk virgl \
    PATH="$PATH" JAVA_HOME="$JAVA_HOME" XDG_DATA_HOME="$GAMEDIR" WAYLAND_DISPLAY= \
    java -jar $GAMEDIR/$jar_filename

    #Clean up after ourselves
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
        $ESUDO umount "${mesa_dir}"
        $ESUDO umount "${JAVA_HOME}"
    fi
    pm_finish
    ```

=== "LibGDX"
    ``` bash 
    #!/bin/bash

    # PortMaster preamble
    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}
    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi
    source $controlfolder/control.txt
    get_controls

    # Adjust these to your paths and desired java version
    GAMEDIR=/$directory/ports/your_port_folder
    java_runtime="zulu17.54.21-ca-jre17.0.13-linux"
    jar_filename="YourGame.jar"
    gptk_filename="YourControls.gptk"

    # Logging
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Create directory for save files
    CONFDIR="$GAMEDIR/conf/"
    $ESUDO mkdir -p "${CONFDIR}"

    # Mount Weston runtime
    weston_dir=/tmp/weston
    $ESUDO mkdir -p "${weston_dir}"
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    # Mount Java runtime
    export JAVA_HOME="/tmp/javaruntime/"
    $ESUDO mkdir -p "${JAVA_HOME}"
    if [ ! -f "$controlfolder/libs/${java_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${java_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${JAVA_HOME}"
    fi
    $ESUDO mount "$controlfolder/libs/${java_runtime}.squashfs" "${JAVA_HOME}"
    export PATH="$JAVA_HOME/bin:$PATH"


    cd $GAMEDIR
    $GPTOKEYB "java" -c "$GAMEDIR/$gptk_filename" &

    # Start Westonpack and Java
    # Put CRUSTY_SHOW_CURSOR=1 after "env" if you need a mouse cursor
    $ESUDO env $weston_dir/westonwrap.sh headless noop kiosk crusty_glx_gl4es \
    PATH="$PATH" JAVA_HOME="$JAVA_HOME" XDG_DATA_HOME="$GAMEDIR" WAYLAND_DISPLAY= \
    java -jar $GAMEDIR/$jar_filename

    #Clean up after ourselves
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
        $ESUDO umount "${JAVA_HOME}"
    fi
    pm_finish
    ```


=== "OpenGL 2 (GLX)"
    **GL4ES:**
    ``` bash 
    #!/bin/bash

    # PortMaster preamble
    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}
    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi
    source $controlfolder/control.txt
    get_controls

    # Adjust these to your paths
    GAMEDIR=/$directory/ports/your_port_folder
    game_executable="your_game.aarch64"
    gptk_filename="YourControls.gptk"
    game_libs=$GAMEDIR/libs.${DEVICE_ARCH}/:$LD_LIBRARY_PATH

    # Logging
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Create directory for save files
    CONFDIR="$GAMEDIR/conf/"
    $ESUDO mkdir -p "${CONFDIR}"

    # Mount Weston runtime
    weston_dir=/tmp/weston
    $ESUDO mkdir -p "${weston_dir}"
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    cd $GAMEDIR
    $GPTOKEYB "$game_executable" -c "$GAMEDIR/$gptk_filename" &

    # Start Westonpack
    # Put CRUSTY_SHOW_CURSOR=1 after "env" if you need a mouse cursor
    $ESUDO env WRAPPED_LIBRARY_PATH=$game_libs \
    $weston_dir/westonwrap.sh headless noop kiosk crusty_glx_gl4es \
    XDG_DATA_HOME=$CONFDIR $GAMEDIR/$game_executable 

    #Clean up after ourselves
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    pm_finish
    ```
    
    **VirGL:**
    ```bash
    #!/bin/bash

    # PortMaster preamble
    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}
    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi
    source $controlfolder/control.txt
    get_controls

    # Adjust these to your paths
    GAMEDIR=/$directory/ports/your_port_folder
    game_executable="your_game.aarch64"
    gptk_filename="YourControls.gptk"
    game_libs=$GAMEDIR/libs.${DEVICE_ARCH}/:$LD_LIBRARY_PATH

    # Logging
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Create directory for save files
    CONFDIR="$GAMEDIR/conf/"
    $ESUDO mkdir -p "${CONFDIR}"

    # Mount Weston runtime
    weston_dir=/tmp/weston
    $ESUDO mkdir -p "${weston_dir}"
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    # Mount Mesa runtime
    mesa_dir=/tmp/mesa
    mesa_runtime="mesa_pkg_0.1"
    if [ ! -f "$controlfolder/libs/${mesa_runtime}.squashfs" ]; then
        if [ ! -f "$controlfolder/harbourmaster" ]; then
            pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
            sleep 5
            exit 1
        fi
        $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${mesa_runtime}.squashfs"
    fi
    $ESUDO mkdir -p "${mesa_dir}"
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${mesa_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${mesa_runtime}.squashfs" "${mesa_dir}"

    cd $GAMEDIR
    $GPTOKEYB "$game_executable" -c "$GAMEDIR/$gptk_filename" &

    # Start Westonpack
    # Put CRUSTY_SHOW_CURSOR=1 after "env" if you need a mouse cursor
    $ESUDO env WRAPPED_LIBRARY_PATH=$game_libs \
    $weston_dir/westonwrap.sh drm gl kiosk virgl \
    XDG_DATA_HOME=$CONFDIR $GAMEDIR/$game_executable 

    #Clean up after ourselves
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    pm_finish
    ```
    

=== "OpenGL ES (EGL/X11))"

    ``` bash 
    #!/bin/bash

    # PortMaster preamble
    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}
    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi
    source $controlfolder/control.txt
    [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"
    get_controls

    # Adjust these to your paths
    GAMEDIR=/$directory/ports/your_port_folder
    game_executable="your_game.aarch64"
    gptk_filename="YourControls.gptk"
    game_libs=$GAMEDIR/libs.${DEVICE_ARCH}/:$LD_LIBRARY_PATH

    # Logging
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Create directory for save files
    CONFDIR="$GAMEDIR/conf/"
    $ESUDO mkdir -p "${CONFDIR}"

    # Mount Weston runtime
    weston_dir=/tmp/weston
    $ESUDO mkdir -p "${weston_dir}"
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    cd $GAMEDIR
    $GPTOKEYB "$game_executable" -c "$GAMEDIR/$gptk_filename" &

    # Start Westonpack
    # Put CRUSTY_SHOW_CURSOR=1 after "env" if you need a mouse cursor
    $ESUDO env WRAPPED_LIBRARY_PATH=$game_libs \
    $weston_dir/westonwrap.sh headless noop kiosk crusty_x11egl \
    XDG_DATA_HOME=$CONFDIR $GAMEDIR/$game_executable 

    #Clean up after ourselves
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    pm_finish
    ```


=== "SDL2"
    **OpenGL 2:**
    ``` bash 
    #!/bin/bash

    # PortMaster preamble
    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}
    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi
    source $controlfolder/control.txt
    [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"
    get_controls

    # Adjust these to your paths
    GAMEDIR=/$directory/ports/your_port_folder
    game_executable="your_game.aarch64"
    gptk_filename="YourControls.gptk"
    game_libs=$GAMEDIR/libs.${DEVICE_ARCH}/:$LD_LIBRARY_PATH
    x11sdl_path="$GAMEDIR/x11sdllib/"
    # Logging
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Create directory for save files
    CONFDIR="$GAMEDIR/conf/"
    $ESUDO mkdir -p "${CONFDIR}"

    # Mount Weston runtime
    weston_dir=/tmp/weston
    $ESUDO mkdir -p "${weston_dir}"
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    cd $GAMEDIR
    $GPTOKEYB "$game_executable" -c "$GAMEDIR/$gptk_filename" &

    # Start Westonpack
    # Put CRUSTY_SHOW_CURSOR=1 after "env" if you need a mouse cursor
    $ESUDO env WRAPPED_LIBRARY_PATH_MALI="$x11sdl_path" WRAPPED_PRELOAD_MALI="$x11sdl_path/libSDL2-2.0.so.0" \
    WRAPPED_LIBRARY_PATH=$game_libs \
    $weston_dir/westonwrap.sh headless noop kiosk crusty_glx_gl4es \
    WAYLAND_DISPLAY= XDG_DATA_HOME=$CONFDIR $GAMEDIR/$game_executable 

    #Clean up after ourselves
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    pm_finish
    ```

    **OpenGL ES:**
    ``` bash 
    #!/bin/bash

    # PortMaster preamble
    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}
    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi
    source $controlfolder/control.txt
    [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"
    get_controls

    # Adjust these to your paths
    GAMEDIR=/$directory/ports/your_port_folder
    game_executable="your_game.aarch64"
    gptk_filename="YourControls.gptk"
    game_libs=$GAMEDIR/libs.${DEVICE_ARCH}/:$LD_LIBRARY_PATH
    x11sdl_path="$GAMEDIR/x11sdllib/"

    # Logging
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Create directory for save files
    CONFDIR="$GAMEDIR/conf/"
    $ESUDO mkdir -p "${CONFDIR}"

    # Mount Weston runtime
    weston_dir=/tmp/weston
    $ESUDO mkdir -p "${weston_dir}"
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    cd $GAMEDIR
    $GPTOKEYB "$game_executable" -c "$GAMEDIR/$gptk_filename" &

    # Start Westonpack
    # Put CRUSTY_SHOW_CURSOR=1 after "env" if you need a mouse cursor
    $ESUDO env WRAPPED_LIBRARY_PATH_MALI="$x11sdl_path" WRAPPED_PRELOAD_MALI="$x11sdl_path/libSDL2-2.0.so.0" \
    SDL_VIDEO_X11_FORCE_EGL=1 WRAPPED_LIBRARY_PATH=$game_libs \
    $weston_dir/westonwrap.sh headless noop kiosk crusty_x11egl \
    WAYLAND_DISPLAY= XDG_DATA_HOME=$CONFDIR $GAMEDIR/$game_executable 

    #Clean up after ourselves
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    pm_finish
    ```

=== "SFML"
    **OpenGL 2:**
    ``` bash 
    #!/bin/bash

    # PortMaster preamble
    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}
    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi
    source $controlfolder/control.txt
    get_controls

    # Adjust these to your paths 
    GAMEDIR=/$directory/ports/your_port_folder
    game_executable="your_game.aarch64"
    gptk_filename="YourControls.gptk"
    game_libs=$GAMEDIR/libs.${DEVICE_ARCH}/:$LD_LIBRARY_PATH

    # Logging
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Create directory for save files
    CONFDIR="$GAMEDIR/conf/"
    $ESUDO mkdir -p "${CONFDIR}"

    # Mount Weston runtime
    weston_dir=/tmp/weston
    $ESUDO mkdir -p "${weston_dir}"
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    cd $GAMEDIR
    $GPTOKEYB "$game_executable" -c "$GAMEDIR/$gptk_filename" &

    # Start Westonpack
    # Put CRUSTY_SHOW_CURSOR=1 after "env" if you need a mouse cursor
    $ESUDO env WRAPPED_LIBRARY_PATH=$game_libs \
    $weston_dir/westonwrap.sh headless noop kiosk crusty_glx_gl4es \
    XDG_DATA_HOME=$CONFDIR $GAMEDIR/$game_executable 

    #Clean up after ourselves
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    pm_finish
    ```

    **OpenGL ES 1.1:**
    ``` bash 
    #!/bin/bash

    # PortMaster preamble
    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}
    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi
    source $controlfolder/control.txt
    get_controls

    # Adjust these to your paths
    GAMEDIR=/$directory/ports/your_port_folder
    game_executable="your_game.aarch64"
    gptk_filename="YourControls.gptk"
    game_libs=$GAMEDIR/libs.${DEVICE_ARCH}/:$LD_LIBRARY_PATH

    # Logging
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Create directory for save files
    CONFDIR="$GAMEDIR/conf/"
    $ESUDO mkdir -p "${CONFDIR}"

    # Mount Weston runtime
    weston_dir=/tmp/weston
    $ESUDO mkdir -p "${weston_dir}"
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    cd $GAMEDIR
    $GPTOKEYB "$game_executable" -c "$GAMEDIR/$gptk_filename" &

    # Start Westonpack
    # Put CRUSTY_SHOW_CURSOR=1 after "env" if you need a mouse cursor
    $ESUDO env CRUSTY_GLES=11 WRAPPED_LIBRARY_PATH=$game_libs \
    WRAPPED_LIBRARY_PATH_MALI=$weston_dir/lib_aarch64/graphics/mesa_x11_stub/ \ 
    $weston_dir/westonwrap.sh headless noop kiosk crusty_x11egl \
    XDG_DATA_HOME=$CONFDIR $GAMEDIR/$game_executable 

    #Clean up after ourselves
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    pm_finish
    ```

    **OpenGL ES 3.1:**
    ``` bash 
    #!/bin/bash

    # PortMaster preamble
    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}
    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi
    source $controlfolder/control.txt
    get_controls

    # Adjust these to your paths
    GAMEDIR=/$directory/ports/your_port_folder
    game_executable="your_game.aarch64"
    gptk_filename="YourControls.gptk"
    game_libs=$GAMEDIR/libs.${DEVICE_ARCH}/:$LD_LIBRARY_PATH

    # Logging
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Create directory for save files
    CONFDIR="$GAMEDIR/conf/"
    $ESUDO mkdir -p "${CONFDIR}"

    # Mount Weston runtime
    weston_dir=/tmp/weston
    $ESUDO mkdir -p "${weston_dir}"
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    cd $GAMEDIR
    $GPTOKEYB "$game_executable" -c "$GAMEDIR/$gptk_filename" &

    # Start Westonpack
    # Put CRUSTY_SHOW_CURSOR=1 after "env" if you need a mouse cursor
    $ESUDO env CRUSTY_GLES=31 WRAPPED_LIBRARY_PATH=$game_libs \
    $weston_dir/westonwrap.sh headless noop kiosk crusty_x11egl \
    XDG_DATA_HOME=$CONFDIR $GAMEDIR/$game_executable 

    #Clean up after ourselves
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    pm_finish
    ```








=== "Xlib"
    ``` bash 
    #!/bin/bash

    # PortMaster preamble
    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}
    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi
    source $controlfolder/control.txt
    get_controls

    # Adjust these to your paths
    GAMEDIR=/$directory/ports/your_port_folder
    game_executable="your_game.aarch64"
    gptk_filename="YourControls.gptk"
    game_libs=$GAMEDIR/libs.${DEVICE_ARCH}/:$LD_LIBRARY_PATH

    # Logging
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Create directory for save files
    CONFDIR="$GAMEDIR/conf/"
    $ESUDO mkdir -p "${CONFDIR}"

    # Mount Weston runtime
    weston_dir=/tmp/weston
    $ESUDO mkdir -p "${weston_dir}"
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    cd $GAMEDIR
    $GPTOKEYB "$game_executable" -c "$GAMEDIR/$gptk_filename" &

    # Start Westonpack
    # Put CRUSTY_SHOW_CURSOR=1 after "env" if you need a mouse cursor
    $ESUDO env WRAPPED_LIBRARY_PATH=$game_libs \
    $weston_dir/westonwrap.sh drm gl kiosk system \
    XDG_DATA_HOME=$CONFDIR $GAMEDIR/$game_executable 

    #Clean up after ourselves
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    pm_finish
    ```

=== "box64"

    ``` bash
    #!/bin/bash

    XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}

    # PortMaster sits in a different folder on each CFW: these four cover every supported one
    if [ -d "/opt/system/Tools/PortMaster/" ]; then
      controlfolder="/opt/system/Tools/PortMaster"
    elif [ -d "/opt/tools/PortMaster/" ]; then
      controlfolder="/opt/tools/PortMaster"
    elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
      controlfolder="$XDG_DATA_HOME/PortMaster"
    else
      controlfolder="/roms/ports/PortMaster"
    fi

    # control.txt: device info ($DEVICE_ARCH, $CFW_NAME, $DISPLAY_WIDTH, $DEVICE_HAS_ARMHF ...), $ESUDO, $GPTOKEYB2, the pm_* helpers
    source $controlfolder/control.txt
    # mod_<CFW>.txt: the per-CFW fixes PortMaster maintains for every port (no CFW checks needed in the script)
    [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"
    # The device's SDL controller mapping, in $sdl_controllerconfig
    get_controls

    GAMEDIR=/$directory/ports/portfolder
    cd $GAMEDIR

    # Everything the script and the game print ends up in log.txt, the file testers send
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # The player's copy of the game (x86_64 Linux build)
    if [ ! -f "$GAMEDIR/gamedata/game.x86_64" ]; then
      pm_message "Copy the Linux version of <Game> into ports/portfolder/gamedata and launch again."
      sleep 5
      pm_finish
      exit 1
    fi
    chmod +x "$GAMEDIR/box64" "$GAMEDIR/gamedata/game.x86_64"

    # Westonpack runtime (downloaded with the port when it is listed in port.json's "runtime")
    weston_dir=/tmp/weston
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    $ESUDO mkdir -p "${weston_dir}"
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
      $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    cd "$GAMEDIR/gamedata"
    export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"

    $GPTOKEYB2 "game.x86_64" -c "$GAMEDIR/game.ini" &
    pm_platform_helper "$GAMEDIR/box64"

    # box64 runs the x86_64 binary; libraries the game needs come from the port folder (never copied into the game files),
    # a Steam stub is preloaded so it wins over the game's own libsteam_api.so
    $ESUDO env CRUSTY_BLOCK_INPUT=1 \
      BOX64_LD_LIBRARY_PATH="$GAMEDIR/libs.x86_64" \
      BOX64_LD_PRELOAD="$GAMEDIR/libsteam_api.so" \
      $weston_dir/westonwrap.sh headless noop kiosk crusty_glx_gl4es \
      XDG_DATA_HOME="$GAMEDIR/conf" \
      "$GAMEDIR/box64" ./game.x86_64

    # Stop Westonpack and unmount it
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
      $ESUDO umount "${weston_dir}"
    fi
    pm_finish
    ```
