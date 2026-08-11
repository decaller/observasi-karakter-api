const request = require('supertest');
const app = require('../app');

describe('v0.3 Submissions Router Endpoints', () => {
  let createdSubmissionId = null;

  it('POST /api/v0.3/submissions should create a submission and return unique ID & timestamp', async () => {
    const response = await request(app)
      .post('/api/v0.3/submissions')
      .send({
        type: 'tb40',
        is_observer: true,
        subject_name: 'Budi Test'
      });

    expect(response.statusCode).toBe(201);
    expect(response.body.id).toBeDefined();
    expect(response.body.saved).toBe(true);
    expect(response.body.timestamp).toBeDefined();
    createdSubmissionId = response.body.id;
  });

  it('POST /api/v0.3/submissions should auto-detect tb40anak for age < 15', async () => {
    const response = await request(app)
      .post('/api/v0.3/submissions')
      .send({
        birth_date: '2015-05-10' // ~11 years old
      });

    expect(response.statusCode).toBe(201);
    expect(response.body.type).toBe('tb40anak');
    expect(response.body.determined_by).toBe('age_detection');
  });

  it('POST /api/v0.3/submissions should auto-detect tb40 for age >= 15', async () => {
    const response = await request(app)
      .post('/api/v0.3/submissions')
      .send({
        birth_date: '1998-03-25' // ~28 years old
      });

    expect(response.statusCode).toBe(201);
    expect(response.body.type).toBe('tb40');
    expect(response.body.determined_by).toBe('age_detection');
  });

  it('GET /api/v0.3/submissions/:id should return submission state, halfway_report, and next_tier', async () => {
    const response = await request(app).get(`/api/v0.3/submissions/${createdSubmissionId}`);
    expect(response.statusCode).toBe(200);
    expect(response.body.id).toBe(createdSubmissionId);
    expect(response.body.halfway_report).toBeDefined();
    expect(response.body.halfway_report.completion_percentage).toBe(0);
    expect(response.body.next_tier).toBeDefined();
    expect(typeof response.body.next_tier).toBe('string');
  });

  it('POST /api/v0.3/submissions/:id/evaluate should save step and return updated halfway_report', async () => {
    const response = await request(app)
      .post(`/api/v0.3/submissions/${createdSubmissionId}/evaluate`)
      .send({
        sequence_number: 1,
        answers: {
          tier_1: { introvert: 60, extrovert: 40 }
        }
      });

    expect(response.statusCode).toBe(200);
    expect(response.body.saved).toBe(true);
    expect(response.body.next_tier).toBe('tier_2');
    expect(response.body.halfway_report.completion_percentage).toBe(25);
  });

  it('PATCH /api/v0.3/submissions/:id/profile should update profile data and auto-detect age', async () => {
    const response = await request(app)
      .patch(`/api/v0.3/submissions/${createdSubmissionId}/profile`)
      .send({
        subject_name: 'Ahmad Profile Updated',
        birth_date: '2016-01-01'
      });

    expect(response.statusCode).toBe(200);
    expect(response.body.saved).toBe(true);
    expect(response.body.subject_name).toBe('Ahmad Profile Updated');
    expect(response.body.type).toBe('tb40anak');
    expect(response.body.determined_by).toBe('age_detection');
  });

  it('PATCH /api/v0.3/submissions/:id/contact should enrich submission with email and phone', async () => {
    const response = await request(app)
      .patch(`/api/v0.3/submissions/${createdSubmissionId}/contact`)
      .send({
        email: 'test@insanmustaqbal.or.id',
        phone: '+6281234567890'
      });

    expect(response.statusCode).toBe(200);
    expect(response.body.updated).toBe(true);
    expect(response.body.contact.email).toBe('test@insanmustaqbal.or.id');
    expect(response.body.contact.phone).toBe('+6281234567890');
  });

  it('GET /api/v0.3/submissions/:id/share should return public view-only result payload with dual result keys', async () => {
    const response = await request(app).get(`/api/v0.3/submissions/${createdSubmissionId}/share`);
    expect(response.statusCode).toBe(200);
    expect(response.body.id).toBe(createdSubmissionId);
    expect(response.body.is_observer).toBe(true);
    expect(response.body.subject_name).toBe('Ahmad Profile Updated');
    // Dual keys: primary `result` and back-compat `results`
    expect(response.body).toHaveProperty('result');
    expect(response.body).toHaveProperty('results');
    expect(response.body).toHaveProperty('halfway_report');
    expect(response.body).toHaveProperty('next_tier');
  });

  it('GET /api/v0.3/events/:eventId/submissions should return array of submissions for event', async () => {
    const response = await request(app).get('/api/v0.3/events/event_test_123/submissions');
    expect(response.statusCode).toBe(200);
    expect(response.body.event_id).toBe('event_test_123');
    expect(Array.isArray(response.body.submissions)).toBe(true);
  });

  it('POST /api/v0.3/submissions should set anonymous submissions to incomplete', async () => {
    const response = await request(app)
      .post('/api/v0.3/submissions')
      .send({ is_anonymous: true, type: 'tb40' });

    expect(response.statusCode).toBe(201);
    expect(response.body.status).toBe('incomplete');
  });

  it('evaluate with increasing sequence_number should not 409 on tier3 multi-part', async () => {
    // Create fresh submission for multi-step flow
    const createRes = await request(app)
      .post('/api/v0.3/submissions')
      .send({ type: 'tb40', is_observer: true, subject_name: 'Seq Test' });
    const sid = createRes.body.id;

    // Tier 1
    const t1 = await request(app)
      .post(`/api/v0.3/submissions/${sid}/evaluate`)
      .send({ sequence_number: 1, answers: { tier_1: { introvert: 50, extrovert: 50 } } });
    expect(t1.statusCode).toBe(200);

    // Tier 2
    const t2 = await request(app)
      .post(`/api/v0.3/submissions/${sid}/evaluate`)
      .send({ sequence_number: 2, answers: { tier_2: ['karsa', 'cipta', 'rasa'] } });
    expect(t2.statusCode).toBe(200);

    // Profile unlock
    await request(app)
      .patch(`/api/v0.3/submissions/${sid}/profile`)
      .send({ subject_name: 'Seq Test', age: 25 });

    // Tier 3 part 1 (seq 3)
    const t3p1 = await request(app)
      .post(`/api/v0.3/submissions/${sid}/evaluate`)
      .send({ sequence_number: 3, answers: { tier_3: { sub_1: 50, sub_2: 60, sub_3: 70 } } });
    expect(t3p1.statusCode).toBe(200);

    // Tier 3 part 2 (seq 4) — must NOT 409
    const t3p2 = await request(app)
      .post(`/api/v0.3/submissions/${sid}/evaluate`)
      .send({ sequence_number: 4, answers: { tier_3: { sub_4: 50, sub_5: 60, sub_6: 70 } } });
    expect(t3p2.statusCode).toBe(200);
    expect(t3p2.body.next_tier).toBeDefined();
  });

  it('GET /api/v0.3/submissions/:id after evaluate should expose next_tier matching evaluate response', async () => {
    const getRes = await request(app).get(`/api/v0.3/submissions/${createdSubmissionId}`);
    expect(getRes.statusCode).toBe(200);
    expect(getRes.body.next_tier).toBeDefined();
    // After profile was updated (tier_1 answers only), next_tier should be tier_2
    expect(getRes.body.next_tier).toBe('tier_2');
  });
});
