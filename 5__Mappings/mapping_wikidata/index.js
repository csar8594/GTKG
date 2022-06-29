const parser = require('rocketrml');

const doMapping = async () => {
  const options = {
    compress: {
        '@vocab': "https://schema.org/"
    },
    toRDF: true,
    verbose: true,
    xmlPerformanceMode: false,
    replace: false,
    ignoreEmptyStrings: true,
  };
  const result = await parser.parseFile('./mapping.ttl', './mapping_results.n3', options).catch((err) => { console.log(err); });
  //console.log(result);
};

doMapping();