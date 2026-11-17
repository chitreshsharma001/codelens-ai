const { CI_API_V4_URL: api, CI_PROJECT_ID: project, CI_MERGE_REQUEST_IID: mr, GITLAB_BOT_TOKEN: token } = process.env;
if (![api, project, mr, token].every(Boolean)) {
  console.log('Required CI variables missing. Skipping review simulation.');
} else {
  try {
    const response = await fetch(`${api}/projects/${project}/merge_requests/${mr}/notes`, {
      method: 'POST', headers: { 'PRIVATE-TOKEN': token, 'Content-Type': 'application/json' },
      body: JSON.stringify({ body: '**CodeLens AI Review Simulation**\n\nThis is a CI workflow demonstration. No AI code review has been performed. Run backend tests and review the changes before merging.' }),
      signal: AbortSignal.timeout(10_000),
    });
    await response.body?.cancel();
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    console.log(`Review simulation posted to MR !${mr}`);
  } catch (error) { console.error(error.message); process.exitCode = 1; }
}
