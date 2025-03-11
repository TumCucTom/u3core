# Frontend Web-APP
 See at [ai.u3core.com](https://ai.u3core.com)

## Contributing

### Figma designs
You can see the outline in the [docs](../../docs/frontend) and
the [Figma Link](https://www.figma.com/design/0JBvMzvd6paWzBFzhuWlZX/U3-Core-App)
for progress on the UI.

### Run and Test
To open the web app, run the following in your terminal:
```
    cd web-app
    npm i
    npm run dev
```

### Deployment
- The website is deployed with [the frontend workflow](../../../.github/workflows/deploy-frontend.yml)
- The website is deployed to the [gh-pages branch](https://github.com/spe-uob/2024-MLAIPredictionMicroservices/tree/gh-pages)
- Then uses FTP to upload the build website to bluehost to display at [ai.u3core.com](https:www.ai.u3core.com)

### Web App
- Find all pages by:
```angular2html
cd web-app/src/pages
```
- Find all layouts by:
```angular2html
cd web-app/src/layouts
```
- Add public assets in:
```angular2html
cd web-app/src/assets
```
- To make a web page at ai.u3core.com/webpagename:
```angular2html
cd web-app/src/router/routes.js
```
- Build the page for deployment with:
```angular2html
quasar build
```

