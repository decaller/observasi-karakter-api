var Handlebars = require('handlebars');

function renderTemplate(template, data) {
  // console.log(template,data);
  var compiledTemplate = Handlebars.compile(template);
  return compiledTemplate(data);
}

module.exports = renderTemplate;

// var renderTemplate = require('./utils/templateRenderer');

// // Sample template
// var template = `
//   <h1>{{title}}</h1>
//   <p>{{description}}</p>
//   <ul>
//     {{#each items}}
//       <li>{{this}}</li>
//     {{/each}}
//   </ul>
// `;

// // Sample data
// var data = {
//   title: 'My Sample Template',
//   description: 'This is a simple example of using Handlebars with Node.js.',
//   items: ['Item 1', 'Item 2', 'Item 3']
// };

// // Render the template with the data
// var renderedHtml = renderTemplate(template, data);

// // Output the rendered HTML
// console.log(renderedHtml);