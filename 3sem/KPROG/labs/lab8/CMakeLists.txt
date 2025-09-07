cmake_minimum_required(VERSION 3.24.1)

# This tells cmake we have goodies in the /cmake folder
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include (PamplejuceVersion)

set(PROJECT_NAME "TEST")

set(PRODUCT_NAME "Pasechnik Plugin")

set(COMPANY_NAME "Pasechnik Company")

set(BUNDLE_ID "com.Psechnik")

# Valid choices: AAX Unity VST VST3 AU AUv3 Standalone
set(FORMATS Standalone)

project(${PROJECT_NAME} VERSION ${CURRENT_VERSION})

include(JUCEDefaults)

add_subdirectory(JUCE)

juce_add_plugin("${PROJECT_NAME}"
    # Icons for the standalone app
    ICON_BIG "${CMAKE_CURRENT_SOURCE_DIR}/packaging/icon.png"

    # Change me!
    COMPANY_NAME "${COMPANY_NAME}"
    BUNDLE_ID "${BUNDLE_ID}"

    # On MacOS, plugin is copied to ~/Users/yourname/Library/Audio/Plug-Ins/
    COPY_PLUGIN_AFTER_BUILD TRUE

    PLUGIN_MANUFACTURER_CODE Pamp

    # Change me!
    # A unique four-character plugin id
    # Note: this must have at least one upper-case character
    PLUGIN_CODE P228
    FORMATS "${FORMATS}"

    # The name of your final executable
    # This is how it's listed in the DAW
    # This can be different from PROJECT_NAME and can have spaces!
    # You might want to use v${MAJOR_VERSION} here once you go to v2...
    PRODUCT_NAME "${PRODUCT_NAME}")

add_library(SharedCode INTERFACE)

target_compile_features(SharedCode INTERFACE cxx_std_20)
enable_language(C ASM_MASM)

set(SourceFiles Source/PluginEditor.h Source/PluginProcessor.h Source/PluginEditor.cpp Source/PluginProcessor.cpp Source/test.asm)
#file(GLOB_RECURSE SourceFiles CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/source/*.cpp" "${CMAKE_CURRENT_SOURCE_DIR}/source/*.h")
target_sources(SharedCode INTERFACE ${SourceFiles})

include(Assets)

# This is where you can set preprocessor definitions for JUCE and your plugin
target_compile_definitions(SharedCode
    INTERFACE

    # JUCE_WEB_BROWSER and JUCE_USE_CURL off by default
    JUCE_WEB_BROWSER=0  # If you set this to 1, add `NEEDS_WEB_BROWSER TRUE` to the `juce_add_plugin` call
    JUCE_USE_CURL=0     # If you set this to 1, add `NEEDS_CURL TRUE` to the `juce_add_plugin` call
    JUCE_VST3_CAN_REPLACE_VST2=0

    # Uncomment if you are paying for a an Indie/Pro license or releasing under GPLv3
    # JUCE_DISPLAY_SPLASH_SCREEN=0

    # lets the app known if we're Debug or Release
    CMAKE_BUILD_TYPE="${CMAKE_BUILD_TYPE}"
    VERSION="${CURRENT_VERSION}"

    # JucePlugin_Name is for some reason doesn't use the nicer PRODUCT_NAME
    PRODUCT_NAME_WITHOUT_VERSION="Test"
)

target_link_libraries(SharedCode
    INTERFACE
    Assets
    juce_audio_utils
    juce_audio_processors
    juce_dsp
    juce_gui_basics
    juce_gui_extra
    juce::juce_recommended_config_flags
    juce::juce_recommended_lto_flags
    juce::juce_recommended_warning_flags)

# Link the JUCE plugin targets our SharedCode target
target_link_libraries("${PROJECT_NAME}" PRIVATE SharedCode)

# Everything related to the tests target
include(Tests)

# A separate target keeps the Tests target fast!
include(Benchmarks)

# Pass some config to GA (like our PRODUCT_NAME)
include(GitHubENV)
