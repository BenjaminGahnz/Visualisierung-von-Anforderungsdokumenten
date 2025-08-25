package org.getaviz.generator;

import org.getaviz.generator.city.m2m.City2City;
import org.getaviz.generator.city.m2t.City2AFrame;
import org.getaviz.generator.city.s2m.JQA2City;
import org.getaviz.generator.jqa.*;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;


import java.util.List;

public class StepFactory {

    private SettingsConfiguration.OutputFormat outputFormat;
    private SettingsConfiguration.Metaphor metaphor;
    private SettingsConfiguration config;
    private List<ProgrammingLanguage> languages;
    private Log log = LogFactory.getLog(StepFactory.class);

    public StepFactory(SettingsConfiguration config, List<ProgrammingLanguage> languages) {
        this.outputFormat = config.getOutputFormat();
        this.metaphor = config.getMetaphor();
        this.config = config;
        this.languages = languages;
    }

    public Step createMetadataFileStep() {
        if(languages.contains(ProgrammingLanguage.JAVA)) {
            return new JQA2JSON(config, languages);
        } else {
            log.info("No languages found");
            return null;
        }
    }

    public Step createSteps2m() {
        if(metaphor == SettingsConfiguration.Metaphor.CITY) {
            if(languages.contains(ProgrammingLanguage.JAVA)) {
            return new JQA2City(config, languages);
            }
            else {
                log.info("No languages found");
                return null;
            }
        }else {
                log.info("No languages found");
                return null;
            }
        }
    
    
    public Step createStepm2m() {
        if(metaphor == SettingsConfiguration.Metaphor.RD) {
            return null;
        } else {
            return new City2City(config);
        }
    }

    public Step createStepm2t() {
        if(outputFormat == SettingsConfiguration.OutputFormat.AFrame) {
            if(metaphor == SettingsConfiguration.Metaphor.RD) {
                return null;
            } else {
                return new City2AFrame(config);
            }
        } else {
            log.info("Nolonger available");
            return null;
        }
    }
}
