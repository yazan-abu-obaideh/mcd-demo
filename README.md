# Introduction
MCD-Demo is a website designed to show the capabilities of the [MCD framework](https://github.com/Lyleregenwetter/Multiobjective-Counterfactuals-for-Design). It offers users a simple 
UI where they can request various optimizations for designs and end up with rendered images of their designs as well as CAD files.

# Technology

MCD-Demo primarily uses Python & Flask in the backend. The frontend is built with HTML, CSS, and TypeScript.
Docker is used for deployment.

# Deployment Guide
1. Checkout the git branch: `server`
2. Obtain SSL certificates for the domain name https://mcd-demo.net and place the certificates under ./nginx/secrets
3. You should have two files in the ./nginx/secrets directory: fullchain.pem and privkey.pem
4. Navigate to ./deployment
5. Run ./deploy.sh (for deploying on Windows, run the single command inside the deploy.sh file)
6. Run `docker container ls`
7. You should see multiple instances of mcd-demo_rendering and mcd-demo_optimization, one instance of mcd-demo_gateway, and one instance of mcd-demo_frontend
