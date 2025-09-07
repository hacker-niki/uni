#pragma once

#include <juce_audio_processors/juce_audio_processors.h>

#if (MSVC)
    #include "ipps.h"
#endif

extern "C" float EchoControl (float sample, float sample_for_echo);
extern "C" float BalanceControl (float sample, float chanel_loudness);
extern "C" float LoudnessControl (float sample, float loudness);
extern "C" float EchoHandle (float sample, float count_echo_handle);

class PluginProcessor : public juce::AudioProcessor
{
public:
    PluginProcessor();
    ~PluginProcessor() override;

    void prepareToPlay (double sampleRate, int samplesPerBlock) override;
    void releaseResources() override;

    bool isBusesLayoutSupported (const BusesLayout& layouts) const override;

    void processBlock (juce::AudioBuffer<float>&, juce::MidiBuffer&) override;

    juce::AudioProcessorEditor* createEditor() override;
    bool hasEditor() const override;

    const juce::String getName() const override;

    bool acceptsMidi() const override;
    bool producesMidi() const override;
    bool isMidiEffect() const override;
    double getTailLengthSeconds() const override;

    int getNumPrograms() override;
    int getCurrentProgram() override;
    void setCurrentProgram (int index) override;
    const juce::String getProgramName (int index) override;
    void changeProgramName (int index, const juce::String& newName) override;

    void getStateInformation (juce::MemoryBlock& destData) override;
    void setStateInformation (const void* data, int sizeInBytes) override;

    //AHTUNG!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    //РУЧКИ
    float loudness = 1.0;
    float left_loudness = 1.0;
    float right_loudness = 1.0;
    int skip_buffers = 100;
    int intens = 10;
    //РУЧКИ
    //AHTUNG!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

private:
    std::deque<float> const_buf;
    const int const_buf_size = 500000;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (PluginProcessor)
};
