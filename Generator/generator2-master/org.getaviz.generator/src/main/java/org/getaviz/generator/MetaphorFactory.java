package org.getaviz.generator;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import java.util.List;
import org.getaviz.generator.city.CityMetaphor;

class MetaphorFactory {
    static Log log = LogFactory.getLog(MetaphorFactory.class);
    static Metaphor createMetaphor(SettingsConfiguration config, List<ProgrammingLanguage> languages) {
        if( config.getMetaphor() == SettingsConfiguration.Metaphor.CITY) {
            return new CityMetaphor(config, languages);
        }
        else {log.info("No City found");
            return null ;
        }
    }
}
