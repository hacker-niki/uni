#include "PluginEditor.h"

PluginEditor::PluginEditor (PluginProcessor& p)
    : AudioProcessorEditor (&p), processorRef (p)
{
    juce::ignoreUnused (processorRef);

    addAndMakeVisible (right);
    addAndMakeVisible (left);
    addAndMakeVisible (left_label);
    addAndMakeVisible (right_label);
    addAndMakeVisible (volume_slider);
    addAndMakeVisible (volume_label);
    addAndMakeVisible (effect1_slider);
    addAndMakeVisible (effect2_slider);
    addAndMakeVisible (effect1_label);
    addAndMakeVisible (effect2_label);

    effect1_slider.setNumDecimalPlacesToDisplay (0);
    effect1_slider.setSliderStyle (juce::Slider::SliderStyle::RotaryVerticalDrag);
    effect1_slider.setRange (10, 1000);
    effect1_slider.setValue (10);

    //TODO
    effect1_slider.onValueChange = [this]() { processorRef.skip_buffers = effect1_slider.getValue(); };

    effect2_slider.setNumDecimalPlacesToDisplay (0);
    effect2_slider.setSliderStyle (juce::Slider::SliderStyle::RotaryVerticalDrag);
    effect2_slider.setRange (1, 20);
    effect2_slider.setValue (1);

    //TODO
    effect2_slider.onValueChange = [this]() { processorRef.intens = effect2_slider.getValue(); };

    volume_slider.setNumDecimalPlacesToDisplay (0);
    volume_slider.setSliderStyle (juce::Slider::SliderStyle::RotaryVerticalDrag);
    volume_slider.setRange (0, 100, 1);
    volume_slider.setValue (50);

    //TODO
    volume_slider.onValueChange = [this]() { processorRef.loudness = volume_slider.getValue() / 100; };

    right.setNumDecimalPlacesToDisplay (0);
    right.setRange (0, 100);
    right.setValue (50);

    //TODO
    right.onValueChange = [&]() { processorRef.right_loudness = right.getValue() / 100; };

    left.setNumDecimalPlacesToDisplay (0);
    left.setRange (0, 100);
    left.setValue (50);

    //TODO
    left.onValueChange = [&]() { processorRef.left_loudness = left.getValue() / 100; };

    right_label.setText ("RIGHT channel", juce::dontSendNotification);
    left_label.setText ("LEFT channel", juce::dontSendNotification);
    volume_label.setText ("VOLUME", juce::dontSendNotification);
    effect1_label.setText ("EFFECT 1", juce::dontSendNotification);
    effect2_label.setText ("EFFECT 2", juce::dontSendNotification);

    // this chunk of code instantiates and opens the melatonin inspector

    // Make sure that before the constructor has finished, you've set the
    // editor's size to whatever you need it to be.
    setSize (600, 400);
}

PluginEditor::~PluginEditor()
{
}

void PluginEditor::paint (juce::Graphics& g)
{
    // (Our component is opaque, so we must completely fill the background with a solid colour)
}

void PluginEditor::resized()
{
    left.setSize (150, 50);
    left.setTopLeftPosition (50, 300);
    left.moved();

    right.setSize (150, 50);
    right.setTopLeftPosition (50, 350);
    right.moved();

    left_label.setSize (100, 30);
    left_label.setTopLeftPosition (50, 290);
    left_label.moved();

    right_label.setSize (100, 30);
    right_label.setTopLeftPosition (50, 340);
    right_label.moved();

    volume_slider.setSize (150, 150);
    volume_slider.setTopLeftPosition (300, 220);
    volume_slider.moved();

    volume_label.setSize (100, 30);
    volume_label.setTopLeftPosition (300, 240);
    volume_label.moved();

    effect1_slider.setSize (150, 150);
    effect1_slider.setTopLeftPosition (30, 60);
    effect1_slider.moved();

    effect1_label.setSize (100, 30);
    effect1_label.setTopLeftPosition (100, 80);
    effect1_label.moved();

    effect2_slider.setSize (150, 150);
    effect2_slider.setTopLeftPosition (400, 60);
    effect2_slider.moved();

    effect2_label.setSize (100, 30);
    effect2_label.setTopLeftPosition (400, 80);
    effect2_label.moved();
    // layout the positions of your child components here
}