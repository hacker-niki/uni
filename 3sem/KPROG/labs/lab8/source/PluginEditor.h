#pragma once

#include "PluginProcessor.h"
#include "BinaryData.h"
// #include "melatonin_inspector/melatonin_inspector.h"

//==============================================================================
class PluginEditor : public juce::AudioProcessorEditor
{
public:
    explicit PluginEditor (PluginProcessor&);
    ~PluginEditor() override;

    //==============================================================================
    void paint (juce::Graphics&) override;
    void resized() override;

private:
    // This reference is provided as a quick way for your editor to
    // access the processor object that created it.
    PluginProcessor& processorRef;
    juce::Slider left;
    juce::Slider right;
    juce::Slider volume_slider;
    juce::Slider effect1_slider;
    juce::Slider effect2_slider;

    juce::Label effect1_label;
    juce::Label effect2_label;
    juce::Label left_label;
    juce::Label right_label;
    juce::Label volume_label;



    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (PluginEditor)
};