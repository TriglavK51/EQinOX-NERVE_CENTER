import * as http from "http";
import * as vscode from "vscode";

const discoveryUrl = "http://127.0.0.1:8088/.well-known/tools";

function discover(): Promise<string> {
  return new Promise((resolve, reject) => {
    const request = http.get(discoveryUrl, { timeout: 2000 }, response => {
      let data = "";
      response.on("data", chunk => (data += chunk));
      response.on("end", () => resolve(data));
    });
    request.on("error", reject);
    request.on("timeout", () => request.destroy(new Error("Nerve Center did not respond")));
  });
}

export function activate(context: vscode.ExtensionContext): void {
  context.subscriptions.push(vscode.commands.registerCommand("nerveCenter.runTool", async () => {
    try {
      const document = JSON.parse(await discover()) as { tools?: Array<{ name: string }> };
      const names = document.tools?.map(tool => tool.name).join(", ") || "no tools";
      void vscode.window.showInformationMessage(`Nerve Center discovered: ${names}`);
    } catch (error) {
      void vscode.window.showErrorMessage(`Nerve Center discovery failed: ${String(error)}`);
    }
  }));
}

export function deactivate(): void {}